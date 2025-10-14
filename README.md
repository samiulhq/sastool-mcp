# sastool — A Tiny MCP Server for Running SAS Code via SASPy

This repository contains a minimal **Model Context Protocol (MCP)** server that exposes two SAS-powered tools to an MCP-compatible client (e.g., Claude Desktop):

- `listlibraries` — lists assigned SAS libraries (including CAS libs)
- `runsascode` — executes SAS code and returns SAS log and listing output

It’s built with `FastMCP` and `saspy`.

---
## ⚙️ Features

- ✅ Clean MCP through SAS log and listing output
- ✅ Returns `LOG` and `LST` from SASPy
- ✅ Easy integration with Claude Desktop
