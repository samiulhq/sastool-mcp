# server.py
from mcp.server.fastmcp import FastMCP
from typing import List
import io, os, sys, contextlib
import saspy
from typing import TypedDict
# Create an MCP server
mcp = FastMCP("sastool")

@contextlib.contextmanager
def silence_all_output():
    # Python-level
    sink_out, sink_err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(sink_out), contextlib.redirect_stderr(sink_err):
        # FD-level
        devnull_path = os.devnull
        with open(devnull_path, 'w') as dn:
            # flush and dup original fds
            sys.stdout.flush(); sys.stderr.flush()
            old_out_fd = os.dup(1)
            old_err_fd = os.dup(2)
            try:
                os.dup2(dn.fileno(), 1)  # redirect fd1 -> devnull
                os.dup2(dn.fileno(), 2)  # redirect fd2 -> devnull
                yield
            finally:
                # restore fds
                os.dup2(old_out_fd, 1)
                os.dup2(old_err_fd, 2)
                os.close(old_out_fd)
                os.close(old_err_fd)

class SASRunResult(TypedDict):
    LOG: str
    LST: str  # “listing” text; will be '' when using HTML ODS



# Add an addition tool
@mcp.tool()
def listlibraries() -> List[str]:
    """List assigned SAS libraries and CAS librarires"""
    # Do *everything* SAS-related inside the silencer, including the import
    try:
        with silence_all_output():
            import saspy
            sas = saspy.SASsession()          # may emit banners
            sas.submit("cas; caslib _ALL_ assign;")  # may emit logs
            libs = sas.assigned_librefs()     # may emit logs
            sas.endsas()
    except Exception as e:
        # Return a JSON-serializable error; do not print
        return [f"SAS session error: {type(e).__name__}: {e}"]

    # Normalize to list[str] for MCP JSON serialization
    if isinstance(libs, dict):
        return [str(k) for k in libs.keys()]

    out: List[str] = []
    for item in (libs or []):
        if isinstance(item, (list, tuple)) and item:
            out.append(str(item[0]))
        else:
            out.append(str(item))
    return out
@mcp.tool()
def runsascode(code: str) -> SASRunResult:
    """Run SAS code provided by user"""""
    # Do *everything* SAS-related inside the silencer, including the import
    try:
        with silence_all_output():
            import saspy
            sas = saspy.SASsession()          # may emit banners
            result=sas.submit(code, results='HTML')
            sas.endsas()
    except Exception as e:
        # Return a JSON-serializable error; do not print
        return [f"SAS session error: {type(e).__name__}: {e}"]

  
    return result


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    # This actually starts the MCP server over stdio for Claude Desktop
    # mcp.run(transport="streamable-http")
    mcp.run()