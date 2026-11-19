# GTA 6 is out. No PC version. So Claude built a game that runs in a browser tab

*Grand Theft Auto VI launched on November 19, 2026. While everyone waits for the download, here's a free, fan-made neon driving game that Claude wrote. You can play it on your phone in 2 seconds.*

**▶ Play NEON COAST:** https://htmlpreview.github.io/?https://github.com/yepishynvladyslav/octanewire-guides/blob/main/games/neon-coast/index.html

## The facts about GTA 6 launch day

- **Release:** Thursday, November 19, 2026 ([Rockstar Newswire](https://www.rockstargames.com/newswire/article/ak3ak31a49a221/grand-theft-auto-vi-is-now-set-to-launch-november-19-2026)).
- **Price:** $79.99 Standard, $99.99 Ultimate.
- **Platforms:** PS5 and Xbox Series X|S only. There's no PC version announced.
- **Storage:** at least 212 GB on PS5.

(Price, platform and size details as compiled by [Tech Insider](https://tech-insider.org/gta-6-release-date-november-19-2026-confirmed/) from the PlayStation, Xbox and Rockstar store pages.)

## What Claude built

NEON COAST is an original top-down arcade game:

- A neon coastal city at night, with a beach and an ocean on the east side.
- A pink car with arcade physics: you can drift and leave skid marks.
- Cash bags on the streets. Every bag raises your heat (1 to 5 stars).
- Police cars that chase you along the road grid. Stop for too long next to one and you're **BUSTED**.
- Tall buildings drawn with fake 3D (parallax), streetlights, and headlights.
- Controls: arrows or WASD to drive, Space to drift. On a phone you get on-screen buttons.

It's **one HTML file**, about 150 KB, with no engine, no downloads and no install. It's pure JavaScript and Canvas 2D.

The video uses the game's own demo autopilot, so that's real gameplay, recorded frame by frame.

## Make your own

You don't need to code. Paste this into Claude and change the theme to whatever you like:

```
Build me a complete browser game as ONE self-contained HTML file (no libraries, no external files).

Theme: top-down arcade driving in a neon coastal city at night.
- City on a road grid, buildings with fake 3D parallax and neon roof edges, streetlights, palm trees, ocean on one side.
- Player car with arcade physics: acceleration, steering that depends on speed, a drift/handbrake button, skid marks.
- Collectibles on the road. Each pickup adds money and raises a 1–5 star "heat" level.
- Enemy cars that chase the player along the roads. Getting pinned for 2 seconds = game over, with a restart screen.
- HUD: money counter, stars, speed.
- Controls: arrows/WASD + Space, plus on-screen touch buttons on phones.
- Use a fixed 60 Hz physics step so it runs the same on every device.
Make it look great: dark background, neon pink/cyan/amber palette, glow effects.
Make it original: no real game names, logos, characters or places.
```

Then open the file in your browser. If something feels off ("the cops get stuck on corners", "the car turns too fast"), tell Claude in plain words and ask it to fix that.

## Fair note

NEON COAST is a fan-made original. It's not affiliated with Rockstar Games or Take-Two, and it doesn't use any of their names, art, characters or code. It's a 150 KB arcade toy, not a replacement for a game that took years to make. It does show how fast you can now go from an idea to something people actually play.

---

*Written by [OctaneWire](https://x.com/OctaneWire). Tech, AI, markets. The signal, explained.*
