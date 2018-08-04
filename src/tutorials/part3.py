"""Add assimilators and basic expansion logic"""
import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR


class JanusBot(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.expand()

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

    """Build assimilators wherever we can build them closest"""
    async def build_assimilators(self):
        for nexus in self.units(NEXUS).ready:
            vespenes = self.state.vespene_geyser.closer_than(15.0, nexus)
            for vespene in vespenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vespene.position)
                if worker is None:
                    break
                # if we can't find a close assim, grab a worker that will build it
                if not self.units(ASSIMILATOR).closer_than(1.0, vespene).exists:
                    await self.do(worker.build(ASSIMILATOR, vespene))

    """Logic for expanding"""
    async def expand(self):
        if self.units(NEXUS).amount < 3 and self.can_afford(NEXUS):
            await self.expand_now()


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, JanusBot()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=False)
