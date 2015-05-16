 
from typed_objects import TypedWritable
from texture import SamplerState

 class RenderAttrib(TypedWritable):
    bam_type_name = "RenderAttrib"


class TransparencyAttrib(RenderAttrib):
    bam_type_name = "TransparencyAttrib"

    M_none = 0
    M_alpha = 1
    M_notused = 2
    M_multisample = 3
    M_multisample_mask = 4
    M_binary = 5
    M_dual = 6

    def __init__(self):
        super().__init__()

        self.mode = self.M_none

    def write_datagram(self, manager, dg):
        super().write_datagram(manager, dg)

        dg.add_int8(self.mode)

class TextureAttrib(RenderAttrib):
    bam_type_name = "TextureAttrib"

    # textureAttrib.h:StageNode
    class StageNode:
        def __init__(self):
            self.sampler = None
            self.stage = None
            self.texture = None
            self.has_sampler = False
            self.ff_tc_index = 0
            self.implicit_sort = 0
            self.override = 0

    def __init__(self):
        super().__init__()

        self._off_all_stages = False
        self.off_stage_nodes = []
        self.on_stage_nodes = []
        self.texture = None

    def write_datagram(self, manager, dg):
        super().write_datagram(manager, dg)

        dg.add_bool(self._off_all_stages)
        dg.add_uint16(len(self.off_stages))
        
        for stage_node in self.off_stage_nodes:
            assert isinstance(stage_node, TextureAttrib.StageNode)
            assert isinstance(stage_node.stage, TextureStage)
            manager.write_pointer(dg, stage)

        dg.add_uint16(len(self.on_stages))

        for stage_node in self.on_stage_nodes:
            assert isinstance(stage_node, TextureAttrib.StageNode)
            assert isinstance(stage_node.stage, TextureStage)
            assert isinstance(stage_node.texture, Texture) 

            manager.write_pointer(dg, stage_node.stage)
            manager.write_pointer(dg, stage_node.texture)

            if manager.file_version >= (6, 15):
                dg.add_uint16(stage_node.implicit_sort)

            if manager.file_version >= (6, 23):
                dg.add_int32(stage_node.override)

            if manager.file_version >= (6, 36):
                dg.add_bool(stage_node.has_sampler)

                if stage_node.has_sampler:
                    assert isinstance(stage_node.sampler, SamplerState)
                    stage_node.sampler.write_datagram(manager, dg)