"""
SPARTAN BIO-VALIDATE
Main entry point - Proxy Mode
"""

import sys
import logging

def main():
    """Main entry point"""
    from spartan_agent import get_server, config
    from api.gateway import app as gateway_app

    print("\n" + "=" * 60)
    print("🔱 SPARTAN BIO-VALIDATE AGENT (UNIFIED PROXY MODE)")
    print("=" * 60 + "\n")

    server = get_server()
    if server:
        # Mount the FastAPI gateway onto the AgentServer's app
        # This allows /endpoint, /validate, /submit to work on the same port
        server._app.mount("/", gateway_app)
        print("✅ Gateway mounted onto AgentServer")
        print("✅ Starting unified server...\n")
        server.run()
    else:
        from spartan_agent import spartan_agent
        print("🔷 Starting in local mode...")
        spartan_agent.run()

if __name__ == "__main__":
    main()
