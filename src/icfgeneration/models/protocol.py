from pydantic import BaseModel, Field
from typing import Optional


class ProtocolSectionMetadata(BaseModel):
    name: Optional[str] = Field(description="The name of the section", default=None)


class ProtocolSection(BaseModel):
    text: str = Field(description="The text of the section")
    metadata: ProtocolSectionMetadata = Field(
        description="The metadata of the section", default=ProtocolSectionMetadata()
    )


class ProtocolMetadata(BaseModel):
    name: Optional[str] = Field(description="The name of the protocol", default=None)
    number: Optional[str] = Field(
        description="The number of the protocol", default=None
    )
    date: Optional[str] = Field(description="The date of the protocol", default=None)
    author: Optional[str] = Field(
        description="The author of the protocol", default=None
    )


class Protocol(BaseModel):
    sections: list[ProtocolSection] = Field(description="The sections of the protocol")
    breadcrumbs: list[str] = Field(
        description="The breadcrumbs of the sections of the protocol"
    )
    parsed_data: str = Field(description="The parsed full text of the protocol")
    metadata: ProtocolMetadata = Field(
        description="The metadata of the protocol", default=ProtocolMetadata()
    )
