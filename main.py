"""
SPARTAN BIO-VALIDATE
Main entry point - Proxy Mode
"""

import sys
import logging

def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("🔱 SPARTAN BIO-VALIDATE AGENT (PROXY MODE)")
    print("=" * 60 + "\n")

    from spartan_agent import spartan_agent, config, run_proxy_mode

    logger = logging.getLogger(__name__)
    logger.info("✅ Agent loaded successfully")
    logger.info(f"✅ Agent Name: {config.agent.name}")
    logger.info(f"✅ Agent Address: {spartan_agent.address}")
    logger.info(f"✅ Proxy Mode: {config.proxy.enabled}")
    
    if config.proxy.enabled:
        logger.info(f"✅ Proxy Endpoint: {config.proxy.endpoint}")
        logger.info(f"✅ Railway Backend: {config.railway.url}")

    print("✅ Agent configured successfully")
    print("✅ Starting agent...\n")

    try:
        run_proxy_mode()
    except KeyboardInterrupt:
        print("\n👋 Agent stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
