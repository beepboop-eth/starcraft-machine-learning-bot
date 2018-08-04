""" Creates a simple bot that creates a game instance and distributes workers"""
import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON


class JanusBot(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()

    """Trains workers as long as we can afford them"""
    async def build_workers(self):
        # for every nexus that's ready
        # noqueue turns off unit queues
        for nexus in self.units(NEXUS).ready.noqueue:
            # if we can afford it, train a probe
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

    """Build pylons next to the first nexus"""
    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    # if we can afford it, place pylon near first nexus
                    await self.build(PYLON, near=nexuses.first)


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, JanusBot()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)
