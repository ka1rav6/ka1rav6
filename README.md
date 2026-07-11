<div align="center">

```
$ ssh kairav@iiitd.edu.in
Connecting... done.
Last login: Sat Jul 11 09:41:12 2026 from 127.0.0.1

$ boot kairav.dev
[  0.001s ] BIOS: IIITD-BTECH-CSE v29 (batch 2029)
[  0.042s ] Mounted /dev/curiosity
[  0.088s ] Loading toolchains: C11 C++20 Python TS JS Asm(x86-64) ..... OK
[  0.140s ] Starting opengl.service ................................... OK
[  0.181s ] Starting rule-engine.service (vela) ....................... OK
[  0.203s ] Starting tensor-lib.service (zcore, zig) .................. OK [experimental]
[  0.240s ] Mounting /mnt/coffee ...................................... OK
[  0.241s ] Coffee cache: warm
[  0.261s ] Checking grass_touching.service ........................... [ WARN ] inactive
[  0.300s ] Running self-test: chess_engine, tetris, textmex ........... PASS
[  0.312s ] system ready.

kairav@iiitd:~$ whoami
```

</div>

# Kairav Dutta

### BTech CSE @ IIIT Delhi ('29) · systems programmer by instinct, ML/AI tinkerer by curiosity

<sub>18 years old, running on caffeine and `make -j$(nproc)`</sub>

[![Portfolio](https://img.shields.io/badge/portfolio-ka1rav6.github.io-black?style=flat-square)](https://ka1rav6.github.io/)
[![Email](https://img.shields.io/badge/email-kairavdutta%40gmail.com-black?style=flat-square)](mailto:kairavdutta@gmail.com)
[![LinkedIn](https://img.shields.io/badge/linkedin-kairavdutta-black?style=flat-square)](https://www.linkedin.com/in/kairavdutta)

</div>

---

## `> navigate`

```
┌─ kairav.dev :: main terminal ──────────────────────────────────────────┐
│                                                                         │
│   [1]  whoami              → About                                    │
│   [2]  man skills           → Tech Stack                              │
│   [3]  ls -la ~/projects    → Projects                                │
│   [4]  cat progress.json    → Live Dashboard  (auto-updates daily)    │
│   [5]  tail -f commits.log  → Recent Updates                          │
│   [6]  ./contact --send     → Get In Touch                            │
│                                                                         │
│   status: online · uptime: since 2007 (no reboots documented)         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Jump to:** [About](#1-whoami) · [Skills](#2-man-skills) · [Projects](#3-ls--la-projects) · [Dashboard](#4-cat-progressjson) · [Updates](#5-tail--f-commitslog) · [Contact](#6-contact---send)

---

## `[1] whoami`

```c
struct kairav {
    char*  college     = "IIIT Delhi, BTech CSE, Batch '29";
    int    age         = 18;
    char*  origin      = "Codeforces CP31 -> systems programming -> game dev -> ML infra";
    char*  currently[] = {"software dev @ Byld IIITD", "ops @ LDA IIITD / IEEE / Cultural Council"};
    float  class_12    = 97.4;  // centum in math
    float  class_10    = 97.6;
    int    jee_air     = 5217;  // somehow.
    bool   ships_things = true;
};
```

I like building things that actually run — a rule engine in C with its own bytecode VM is just as fun to me as spinning up a React + Django app. Started with competitive programming, fell down the rabbit hole of systems programming, OpenGL/SDL2 game dev, language design, and ML — and now I ship VS Code extensions real people install.

---

## `[2] man skills`

| Category | Stack |
|---|---|
| **Languages** | `C (C11/C23)` `C++ (17/20)` `Python` `Java` `TypeScript` `JavaScript` `Assembly (x86-64)` |
| **Frontend/UI** | `React 18/19` `Vite` `Tailwind` `ImGui` `Streamlit` `EzUI` |
| **Backend/DB** | `FastAPI` `Flask` `Django REST` `PostgreSQL` `MongoDB` `Node.js` `SQLite` |
| **Systems & Graphics** | `OpenGL` `GLFW` `SDL2` `Qt 5/6` `Linux` `Sockets` `ASIO` `CMake/Make` |
| **AI/ML** | `PyTorch` `MediaPipe` `OpenCV` `scikit-learn` `NumPy/Pandas` `OR-Tools` |
| **Tooling** | `VS Code Extension API` `Git` `pybind11` `vcpkg` `Zig` |

---

## `[3] ls -la ~/projects`

<table>
<tr><td width="50%" valign="top">

**⚙️ [vela](https://github.com/ka1rav6/vela)**
Embeddable rule engine in C — JSON rules compiled to bytecode, run on a stack-machine VM. Arena allocator, bitmask fact storage, POSIX thread-safe, packaged as `libvela.a`.
`C` `bytecode-vm` `CMake`

</td><td width="50%" valign="top">

**🧮 [zcore](https://github.com/ka1rav6/zcore)**
Tensor library written in Zig — storage/shape/stride primitives first, autograd later. `[IN PROGRESS]`
`Zig` `tensors` `SIMD`

</td></tr>
<tr><td valign="top">

**🎮 [ctf-game](https://github.com/ka1rav6/ctf-game)**
3D capture-the-flag built on OpenGL + GLFW, Assimp model loading, ReactPhysics3D, ImGui debug tooling. `[IN PROGRESS]`
`C++20` `OpenGL` `Physics`

</td><td valign="top">

**📦 [LazyCMake](https://github.com/ka1rav6/lazycmake)**
`lazygit`-inspired TUI for scaffolding & building CMake C/C++ projects, no hand-written `CMakeLists.txt`.
`C++20` `FTXUI` `CMake`

</td></tr>
<tr><td valign="top">

**🔤 [K Language](https://github.com/ka1rav6/K)**
A language that transpiles to C++ — cleaner syntax, better errors, still low-level control. Lexer → Parser → Transpiler.
`Python` `C++` `compilers`

</td><td valign="top">

**🖥️ [HTTP Server](https://github.com/ka1rav6/http-server-cpp)**
HTTP/1.1 server from raw Linux sockets — no external HTTP libs. Manual TCP/IP, parsing, static file serving.
`C++` `Sockets`

</td></tr>
<tr><td valign="top">

**♟️ [Chess Engine](https://github.com/ka1rav6/chess_engine)**
C chess engine — SAN parsing, legality checking, check/checkmate detection.
`C11` `CMake`

</td><td valign="top">

**📟 [Textmex](https://github.com/ka1rav6/text-editor)**
Vim-like terminal text editor. Gap buffer, raw terminal I/O, cursor movement.
`C++` `Terminal I/O`

</td></tr>
</table>

<div align="center">

*24+ repos total — full list on the [portfolio](https://ka1rav6.github.io/#projects) or [pinned repos below](#4-cat-progressjson).*

</div>

---

## `[4] cat progress.json`

<!--START_SECTION:dashboard-->
*(this table is refreshed daily by GitHub Actions — see workflow below)*
<!--END_SECTION:dashboard-->

<div align="center">
<img src="https://github-readme-stats.vercel.app/api?username=ka1rav6&show_icons=true&theme=transparent&hide_border=true&count_private=true" height="165"/>
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=ka1rav6&layout=compact&theme=transparent&hide_border=true" height="165"/>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=ka1rav6&theme=transparent&hide_border=true" height="165"/>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=ka1rav6&theme=github-compact&hide_border=true" width="100%"/>
</div>

---

## `[5] tail -f commits.log`

```
commit 9a2f61c (HEAD -> main)
Author: Kairav Dutta <kairavdutta@gmail.com>
Date:   this week

    feat(zcore): storage/shape/stride primitives
    - core tensor struct laid out, arithmetic ops not implemented yet
    - scoping community traction on Ziggit
    - TODO: broadcasting, autograd, SIMD via @Vector

commit 6c18de4
Date:   recent

    fix(vela): CI/CD pipeline + CMake infra stabilized
    - test suite flakiness fixed
    - libvela.a packaging confirmed reproducible

commit 41ab9f0
Date:   earlier

    feat(game-engine): physics <-> ECS transform sync
    - ReactPhysics3D + EnTT wired together
    - Dear ImGui editor: F1 toggle, GLFW callback chaining
    - added shader cache, fixed collider + shader bugs

commit 2d90a77
Date:   earlier

    feat(wayfinder): AI-powered browser history search
    - Chrome MV3, React + TypeScript, IndexedDB
    - ONNX embeddings running client-side

commit c3fe882
Date:   earlier

    docs(zcore): full tensor library reference + 10-phase roadmap
    - IEEE-754, linear algebra, strides/broadcasting, autograd
    - Zig-specific: comptime generics, allocator ownership

commit 0f1a336
Date:   earlier

    feat(lazycmake): Phase 0/1 core layer implemented + tested
    - dual-surface customization architecture
    - plugin system, event bus, state machines

commit --- (older history)
    chore: chess engine, gesture-recognition game, VS Code extensions,
    ROTA scheduler, and assorted OpenGL bug hunts. see full commit
    graph for the rest.
```

<sub>known bug: occasionally touches grass · severity: low · status: won't fix</sub>

---

## `[6] ./contact --send`

```
$ ./contact --send --to=kairav
> email:     kairavdutta@gmail.com
> github:    github.com/ka1rav6
> linkedin:  linkedin.com/in/kairavdutta
> portfolio: ka1rav6.github.io
> response_time: usually fast, unless mid-refactor
```

<div align="center">
<sub>compiled without warnings · built with ♥ and too much coffee · merge conflicts mostly resolved in real life</sub>
</div>
