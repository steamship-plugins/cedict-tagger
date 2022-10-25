"""Steamship CEDict Tagger Plugin
"""

from typing import Type

from steamship import Block, Tag
from steamship.app import App, create_handler
from steamship.base.error import SteamshipError
from steamship.data.file import File
from steamship.plugin.blockifier import Config
from steamship.plugin.inputs.block_and_tag_plugin_input import \
    BlockAndTagPluginInput
from steamship.plugin.outputs.block_and_tag_plugin_output import \
    BlockAndTagPluginOutput
from steamship.plugin.service import PluginRequest
from steamship.plugin.tagger import Tagger

from cedict_tagger import CeDictTrie, entry_to_dict


class CEDictTaggerPluginConfig(Config):
    pass

class CEDictTaggerPlugin(Tagger, App):

    def config_cls(self) -> Type[CEDictTaggerPluginConfig]:
        return CEDictTaggerPluginConfig

    def run(
        self, request: PluginRequest[BlockAndTagPluginInput]
    ) -> BlockAndTagPluginOutput:
        # TODO: Ensure base Tagger class checks to make sure this is not None
        file = request.data.file

        client = CeDictTrie().load()
        if client is None:
            raise SteamshipError(message="Unable to create CeDictTaggerClient.")

        output = BlockAndTagPluginOutput(file=File.CreateRequest())

        for block in request.data.file.blocks:
            # Create tags for that block via OneAI and add them
            entries = client.tokenize(block.text)
            tags = []

            for start, end, entry in entries:
                tags.append(Tag.CreateRequest(
                    start_idx=start,
                    end_idx=end,
                    kind="token",
                    name="ce-dict",
                    value=entry_to_dict(entry)
                ))

            # Create an output block for this block
            output_block = Block.CreateRequest(id=block.id, tags=tags)

            # Attach the output block to the response
            output.file.blocks.append(output_block)

        return output


handler = create_handler(CEDictTaggerPlugin)
