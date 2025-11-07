from code.extensions import redis_client

def blacklist_token(jti, exp_seconds):
    """
    Store JWT token in Redis blacklist until it expires
    jti: JWT Token ID
    exp_seconds: token lifetime in seconds
    """
    redis_client.setex(name=jti, time=exp_seconds, value="blacklisted")

def is_token_blacklisted(jti):
    """
    Check if a JWT token is blacklisted
    Returns True if blacklisted, else False
    """
    return redis_client.get(jti) is not None
