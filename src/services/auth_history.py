from flask import request
from user_agents import parse

from src.services.auth import get_user_agent


class DeviceType:
    pc = 'pc'
    tablet = 'tablet'
    mobile = 'mobile'
    other = 'other'


def prepare_auth_history_params(current_user) -> dict:
    user_agent = get_user_agent()
    return {
        'user_agent': user_agent,
        'user_id': current_user.id,
        'device_type': _get_type_device(user_agent),
        'ip_address': request.remote_addr
    }


def _get_type_device(user_agent):
    user_agent = parse(user_agent)
    if user_agent.is_pc:
        return DeviceType.pc
    if user_agent.is_tablet:
        return DeviceType.tablet
    if user_agent.is_mobile:
        return DeviceType.mobile
    return DeviceType.other
