from pydantic import BaseModel, Field
from typing import List, Dict, Union, Any
from datetime import datetime
import uuid


class BaseEvent(BaseModel):
    """
    Base model for all activity events.
    """

    session_id: uuid.UUID = Field(
        ...,
        description="Unique identifier for the user session."
    )
    website_id: uuid.UUID = Field(
        ...,
        description="Unique identifier for the website."
    )
    url: str = Field(
        ...,
        description="URL of the webpage where the event occurred."
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of when the event occurred."
    )

    class Config:
        orm_mode = True
        from_attributes = True

class ClickPayload(BaseModel):
    """
    Payload model for click events.
    """

    element_id: str = Field(
        ...,
        description="ID of the HTML element that was clicked."
    )
    element_classes: List[str] = Field(
        default=[],
        description="List of CSS classes of the clicked element."
    )
    position: Dict[str, int] = Field(
        ...,
        description="Position of the click event on the page (x, y coordinates)."
    )

class ScrollPayload(BaseModel):
    """
    Payload model for scroll events.
    """

    scroll_depth_px: int = Field(
        ...,
        description="Depth of the scroll in pixels."
    )
    scroll_depth_percent: float = Field(
        ...,
        description="Depth of the scroll as a percentage."
    )
    viewport_height: int = Field(
        ...,
        description="Height of the viewport in pixels."
    )
    document_height: int = Field(
        ...,
        description="Total height of the document in pixels."
    )

class MouseMovementPayload(BaseModel):
    """
    Payload model for mouse move events.
    """

    positions: List[Dict[str, int]] = Field(
        ...,
        description="List of mouse positions (x, y coordinates) during the event."
    )
    button: str = Field(
        ...,
        description="Mouse button used for the click (e.g., left, right)."
    )
    duration_ms: int = Field(
        ...,
        description="Duration of the mouse movement in milliseconds."
    )

class KeypressPayload(BaseModel):
    """
    Payload model for keypress events.
    """

    key: str = Field(
        ...,
        description="The key that was pressed."
    )
    code: str = Field(
        ...,
        description="The physical key on the keyboard."
    )
    alt_key: bool = Field(
        default=False,
        description="Whether the Alt key was pressed."
    )
    ctrl_key: bool = Field(
        default=False,
        description="Whether the Control key was pressed."
    )
    shift_key: bool = Field(
        default=False,
        description="Whether the Shift key was pressed."
    )
    meta_key: bool = Field(
        default=False,
        description="Whether the Meta key was pressed."
    )
    target_element_id: str = Field(
        ...,
        description="ID of the HTML element that was the target of the keypress."
    )

class WindowResizePayload(BaseModel):
    """
    Payload model for window resize events.
    """

    old_width: int = Field(
        ...,
        description="Old width of the window before resizing."
    )
    old_height: int = Field(
        ...,
        description="Old height of the window before resizing."
    )
    new_width: int = Field(
        ...,
        description="New width of the window after resizing."
    )
    new_height: int = Field(
        ...,
        description="New height of the window after resizing."
    )

class ClickEvent(BaseEvent):
    """
    Model for click events.
    """

    event_type: str = Field(
        default="click",
        description="Type of the event."
    )
    payload: ClickPayload = Field(
        ...,
        description="Payload containing details of the click event."
    )

class ScrollEvent(BaseEvent):
    """
    Model for scroll events.
    """

    event_type: str = Field(
        default="scroll",
        description="Type of the event."
    )
    payload: ScrollPayload = Field(
        ...,
        description="Payload containing details of the scroll event."
    )

class MouseMovementEvent(BaseEvent):
    """
    Model for mouse movement events.
    """

    event_type: str = Field(
        default="mouse_move",
        description="Type of the event."
    )
    payload: MouseMovementPayload = Field(
        ...,
        description="Payload containing details of the mouse movement event."
    )

class KeypressEvent(BaseEvent):
    """
    Model for keypress events.
    """

    event_type: str = Field(
        default="keypress",
        description="Type of the event."
    )
    payload: KeypressPayload = Field(
        ...,
        description="Payload containing details of the keypress event."
    )

class WindowResizeEvent(BaseEvent):
    """
    Model for window resize events.
    """

    event_type: str = Field(
        default="window_resize",
        description="Type of the event."
    )
    payload: WindowResizePayload = Field(
        ...,
        description="Payload containing details of the window resize event."
    )

EventModel = Union[
    ClickEvent,
    ScrollEvent,
    MouseMovementEvent,
    KeypressEvent,
    WindowResizeEvent
]

class BatchEventPayload(BaseModel):
    """
    Model for batching multiple events together.
    """

    events: List[EventModel] = Field(
        ...,
        description="List of activity events."
    )
    class Config:
        orm_mode = True
        from_attributes = True

class BatchEventRequest(BaseModel):
    """
    Model for the batch event request.
    """

    payload: BatchEventPayload = Field(
        ...,
        description="Payload containing a batch of events."
    )
    class Config:
        orm_mode = True
        from_attributes = True

class BatchEventResponse(BaseModel):
    """
    Model for the batch event response.
    """

    success: bool = Field(
        ...,
        description="Indicates if the batch event processing was successful."
    )
    processed_event_count: int = Field(
        ...,
        description="Number of events that were processed."
    )
    message: str = Field(
        ...,
        description="Additional information about the batch processing."
    )
    class Config:
        orm_mode = True
        from_attributes = True

__all__ = [
    "ClickEvent",
    "ScrollEvent",
    "MouseMovementEvent",
    "KeypressEvent",
    "WindowResizeEvent",
    "BatchEventRequest",
    "BatchEventResponse"
]