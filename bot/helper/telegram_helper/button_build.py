from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


_button_init_vars = InlineKeyboardButton.__init__.__code__.co_varnames
_supports_style = "style" in _button_init_vars
_supports_icon_emoji = "icon_custom_emoji_id" in _button_init_vars

def _resolve_userset_style(key, data, style):
    if style or not isinstance(data, str) or not data.startswith("userset"):
        return style

    lower_key = str(key).lower()
    if any(word in lower_key for word in ("close", "reset", "delete", "remove", "disable", "stop", "cancel")):
        return "danger"
    if any(word in lower_key for word in ("enable", "activate", "confirm", "yes")):
        return "success"
    return "primary"


class ButtonMaker:
    def __init__(self):
        self.buttons = {
            "default": [],
            "header": [],
            "f_body": [],
            "l_body": [],
            "footer": [],
        }
    def url_button(
        self,
        key,
        link,
        position=None,
        style=None,
        icon_custom_emoji_id=None,
    ):
        button_kwargs = {"text": key, "url": link}
        if style and _supports_style:
            button_kwargs["style"] = style
        if icon_custom_emoji_id and _supports_icon_emoji:
            button_kwargs["icon_custom_emoji_id"] = icon_custom_emoji_id
        self.buttons[position if position in self.buttons else "default"].append(
            InlineKeyboardButton(**button_kwargs)
        )
    def build_menu(self, b_cols=1, h_cols=8, fb_cols=2, lb_cols=2, f_cols=8):
        def chunk(lst, n):
            return [lst[i : i + n] for i in range(0, len(lst), n)]

        menu = chunk(self.buttons["default"], b_cols)
        menu = (
            chunk(self.buttons["header"], h_cols) if self.buttons["header"] else []
        ) + menu
        for key, cols in (("f_body", fb_cols), ("l_body", lb_cols), ("footer", f_cols)):
            if self.buttons[key]:
                menu += chunk(self.buttons[key], cols)
        return InlineKeyboardMarkup(menu)

    def reset(self):
        for key in self.buttons:
            self.buttons[key].clear()
