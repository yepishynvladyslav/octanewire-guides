# One space wiped a developer's ~/Library. Here's the exact bug, and the 3 rules that stop it

*A coding agent was asked to delete 5 test chat channels. About two minutes later, the user's whole `~/Library` folder was gone.*

## What happened

In November 2026 a developer described this on [r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1xqfp7m/):

- The agent's task was small: clean up 5 test channels.
- It ran with `--dangerously-skip-permissions`, so no command needed approval.
- The paths contained `Application Support`, a folder name with a space in it.
- The command piped paths through `xargs -n1 dirname` before `rm -rf`.
- In roughly two minutes, `~/Library` was deleted. There was no backup at that moment. The poster later said they recovered most of the data.

Our film is a **recreation**. The path is shown as `/Users/you/...` and the clock counts elapsed time (00:00 to 02:00), because we couldn't verify the exact wall-clock times or username.

## The bug, in one line

`xargs` splits its input on whitespace. So this one path:

```
/Users/you/Library/Application Support/AgentThreads/channels/
```

becomes two arguments:

```
/Users/you/Library/Application
Support/AgentThreads/channels/
```

Then `dirname /Users/you/Library/Application` returns:

```
/Users/you/Library
```

And that is what reached `rm -rf`.

## The fix for the command

Never feed paths to `xargs` split on spaces. Use NUL separators:

```bash
find "$DIR" -name 'test-*' -print0 | xargs -0 rm -rf --
```

Or skip `xargs` entirely and quote every path:

```bash
rm -rf -- "$HOME/Library/Application Support/AgentThreads/channels/test-1"
```

## The 3 rules

```
1. Quote paths: find … -print0 | xargs -0
2. Never skip permissions on your real machine.
3. Put a hook between the agent and rm.
```

Rule 2 matters most. `--dangerously-skip-permissions` is fine inside a throwaway container. On the laptop that holds your passwords, it removes the last human checkpoint.

## Rule 3: what a hook does

Claude Code supports **PreToolUse hooks**: a small program that sees every command *before* it runs, and can answer `deny`.

[Seatbelt](https://github.com/yepishynvladyslav/seatbelt) is our free hook. After this case we shipped **v0.5**, which adds a `rm-home-critical` rule: a recursive delete aimed at a whole home folder (`~`, `~/Library`, `~/Documents`, `~/.ssh` and others) is blocked outright, not just flagged.

Real output from v0.5 on the command in the film:

```
⛔ BLOCK  rm -rf "/Users/you/Library"
   rm-home-critical · Recursive delete of a whole home folder (/Users/you/Library). Passwords, settings and app data live here.
```

And the JSON the hook returns to Claude Code:

```json
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
 "permissionDecisionReason": "Seatbelt blocked this [rm-home-critical]: Recursive delete of a whole home folder (/Users/you/Library). Passwords, settings and app data live here."}}
```

A hook is a seatbelt, not a guarantee. It catches the common shapes of a disaster. Backups (Time Machine or any off-machine copy) are still the thing that saves you when everything else fails.

## Install

See the [Seatbelt README](https://github.com/yepishynvladyslav/seatbelt). It's one Python file plus one entry in your Claude Code settings.

---

*Written by [OctaneWire](https://x.com/OctaneWire). Tech, AI, markets. The signal, explained. It asks before it spends.*
