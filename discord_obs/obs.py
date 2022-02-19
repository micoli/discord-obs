import asyncio
import gbulb
import simpleobsws

from discord_obs.configuration import OBSWS_PASSWORD, OBSWS_PORT

asyncio.set_event_loop_policy(gbulb.GLibEventLoopPolicy())


class Obs():
    def __init__(self):
        self.obsws = simpleobsws.WebSocketClient(
            url='ws://localhost:%s' % OBSWS_PORT,
            password=OBSWS_PASSWORD,
            identification_parameters=simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks=False)
        )

    def get_scenes_list(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.async_get_scenes())

    async def async_get_scenes(self):
        await self.obsws.connect()
        await self.obsws.wait_until_identified()
        scenes_result = await self.do_request(simpleobsws.Request('GetSceneCollectionList'))
        await self.obsws.disconnect()
        return scenes_result['sceneCollections']

    def change_scene(self, scene):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_change_scene(scene))

    async def async_change_scene(self, scene):
        await self.obsws.connect()
        await self.obsws.wait_until_identified()
        await self.do_request(simpleobsws.Request('SetCurrentSceneCollection', {'sceneCollectionName': scene}))
        await self.obsws.disconnect()

    async def do_request(self, request):
        ret = await self.obsws.call(request)
        # if ret.ok():
        #    print("Request succeeded! Response data: {}".format(ret.responseData))
        return ret.responseData
