"""Use public DNS for mongodb+srv SRV/TXT lookups when the system resolver (e.g. home router) times out."""


def prefer_public_dns_for_srv(url: str) -> None:
    if not url.lower().startswith("mongodb+srv"):
        return
    try:
        import dns.resolver

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ["8.8.8.8", "8.8.4.4", "1.1.1.1"]
        dns.resolver.default_resolver = resolver
    except ImportError:
        pass
