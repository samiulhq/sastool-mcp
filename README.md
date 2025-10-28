# sastool — A Tiny MCP Server for Running SAS Code via SASPy

This repository contains a minimal **Model Context Protocol (MCP)** server that exposes following SAS-powered tools to an MCP-compatible client (e.g., Claude Desktop, GitHub CoPilot):

| Tool Name | Description |
|------------|-------------|
| `run_sas(code)` | Runs SAS code and returns LOG + HTML results |
| `list_libs()` | Lists assigned SAS/CAS libraries |
| `list_tables(libname)` | Lists tables in a SAS library |
| `list_directory(path)` | Lists files on SAS server | 
| `save_code(path, filename, content)` | Save SAS code remotely |

---
## ⚙️ Features

- ✅ Clean MCP through SAS log and listing output
- ✅ Returns `LOG` and `LST` from SASPy
- ✅ Easy integration with Claude Desktop

## SASPy Configuration
SASPy requires a configuration that specifies how it connects to SAS. To configure SASPy follow the instructions [here](https://sassoftware.github.io/saspy/configuration.html).

## ⚙️ Use with Claude Desktop
### Click to see the demo
[![##Watch the video](https://lh3.googleusercontent.com/d/1WAwX4zkm_tZLN-MwNthcq3kJ57g72uPb=w600-h600)](https://www.loom.com/share/60200b5123604569b64f68519ed527de?sid=de6b7b35-a3a0-4540-8773-668c5c00a002)



Edit your claude_desktop_config.json:
```json
{
  "mcpServers": {
    "sastool": {
      "command": ",/absolute/path/to/.venv/bin/python or uv>",
      "args": ["run", "--with", "mcp[cli]","/absolute/path/to/server.py"],
      "env": {
        "SAS_CONFIG_NAMES": "default",
        "PYTHONUNBUFFERED": "1"
      },
      "disabled": false
    }
  }
}
```
### Example flow with Claude

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant C as Claude Desktop<br/>(Sonnet 4.5)
    participant M as MCP Server<br/>(server.py / FastMCP)
    participant P as SASPy
    participant VC as SAS Viya Compute
    participant CAS as CAS / CASLIBs

    U->>C: Analysis request from user
    C->>C: Generate SAS Code:code
    C->>M: MCP tool call: runsascode(code)
    M->>P: sas.submit(code, results='HTML')
    P->>VC: Start compute session
    VC->CAS: CAS Initiate

    CAS-->>VC: Data access / processing

    VC-->>P: Return LOG and ODS results
    P-->>M: {"LOG": "...", "LST": "<html>...</html>"}
    M-->>C: Return MCP JSON
    C->>C: Evaluate and generate additional SAS code if needed
    C-->>U: Display results (HTML tables/graphs)
```
