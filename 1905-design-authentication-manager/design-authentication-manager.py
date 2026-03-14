class AuthenticationManager:

    def __init__(self, timeToLive: int):
        self.tokens = {}
        self.ttl = timeToLive

    def generate(self, tokenId: str, currentTime: int) -> None:
        self.tokens[tokenId] = currentTime + self.ttl

    def renew(self, tokenId: str, currentTime: int) -> None:
        tok_val = self.tokens.get(tokenId)

        # print(f"refresh {tokenId}-{tok_val} at {currentTime}")
        if tok_val is not None and currentTime < tok_val:
            self.tokens[tokenId] = currentTime + self.ttl
            # print(f"refreshed {tokenId} to {currentTime + self.ttl}")

    def countUnexpiredTokens(self, currentTime: int) -> int:
        exps = list(self.tokens.values())
        exps.sort(reverse=True)

        valid_count = 0
        # print(exps, currentTime)
        for e in exps:
            if currentTime >= e:
                return valid_count
            else:
                valid_count += 1

        return valid_count
        
# Your AuthenticationManager object will be instantiated and called as such:
# obj = AuthenticationManager(timeToLive)
# obj.generate(tokenId,currentTime)
# obj.renew(tokenId,currentTime)
# param_3 = obj.countUnexpiredTokens(currentTime)