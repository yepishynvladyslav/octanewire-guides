# Kit C · Meeting Stand-in

**What it does:** Grok Bot joins a Google Meet, Zoom or Microsoft Teams call, takes notes, answers questions in the meeting chat when someone addresses it by name, and posts a summary with action items when the call ends.

**Plan:** meetings need a **Team, Enterprise or Ultra** plan (xAI docs). On Enterprise, an admin must switch Meetings on.

## Before the meeting: tell people

The bot appears in the call as *"[Bot name] (your first name's Bot) - transcribing"*, and the host has to let it in. xAI's docs don't say whether participants get a separate recording notice, so tell them yourself. Recording rules differ by country and some places require everyone's consent.

Message to send with the invite:

```
Heads-up: my AI assistant (Grok Bot) will join this call to take notes and share a summary afterwards. It will show up as "[Bot name] - transcribing". If you'd rather it didn't join, reply and I'll leave it out.
```

## The prompt

Paste the meeting link into your chat with the bot, then:

```
Join this meeting and take notes.
If someone asks you a question in the meeting chat, answer only from our shared docs and past meeting notes. If you're not sure, say "I'll pass that to [my name]".
Never share files, links or numbers that weren't already shared in this meeting.
After the call, post here:
1. Decisions made
2. Action items: owner + deadline
3. Open questions nobody answered
Don't send the summary to anyone else until I approve it.
```

Approve the card the bot shows, and the host admits it to the call.

## Safety checklist

- [ ] Everyone in the call knows a bot is taking notes
- [ ] Don't use it for HR, legal, medical or salary conversations
- [ ] The summary goes to you first, not straight to the group
- [ ] If the bot is in the call and you need to stop it, use **Quit**. Once it's in, interactivity can only be turned back on by removing and re-adding it.

---

Sources: xAI docs: [Meetings](https://docs.x.ai/grok-bot/meetings), [Approvals, security and privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy)
