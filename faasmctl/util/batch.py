from faasmctl.util.message import message_factory
from faasmctl.util.gen_proto.faabric_pb2 import BatchExecuteRequest, Message
from faasmctl.util.random import generate_gid
from google.protobuf.json_format import ParseDict
import struct

def serialize_string(buffer, string):
    # Serialize the length of the string as a uint32
    buffer.extend(struct.pack('I', len(string)))
    # Serialize the string characters
    buffer.extend(string.encode('utf-8'))

def serialize_map(map_data):
    buffer = bytearray()
    # Serialize the number of key-value pairs as a uint32
    buffer.extend(struct.pack('I', len(map_data)))
    for key, value in map_data.items():
        serialize_string(buffer, key)
        serialize_string(buffer, value)
    return buffer


def batch_exec_factory(req_dict, msg_dict, num_messages):
    req = ParseDict(req_dict, BatchExecuteRequest())
    req.appId = generate_gid()

    for _ in range(num_messages):
        req.messages.append(message_factory(msg_dict, req.appId))

    return req

def batch_exec_input_factory(req_dict, app_id, msg_dict, num_messages, input_list = None, chained_id_list = None):
    req = ParseDict(req_dict, BatchExecuteRequest())
    req.appId = app_id

    if input_list is not None:
        assert len(input_list) == num_messages, "Number of input data should match number of messages"
    
    if chained_id_list is not None:
        assert len(chained_id_list) == num_messages, "Number of chainedIds should match number of messages"
    
    for i in range(num_messages):
        msg = ParseDict(msg_dict, Message())
        msg.appId = app_id
        msg.id = i + 1
        msg.user = req.user
        msg.function = req.function
        if input_list is not None:
            serialized_input = serialize_map(input_list[i])
            msg.inputData = bytes(serialized_input)
        msg.chainedId = chained_id_list[i]
        req.messages.append(msg)
    return req

def batch_messages_input_factory(req_dict, app_id, msg_dict, num_messages, input_list = None, chained_id_list = None):
    req = ParseDict(req_dict, BatchExecuteRequest())
    req.appId = app_id

    if input_list is not None:
        assert len(input_list) == num_messages, "Number of input data should match number of messages"
    
    if chained_id_list is not None:
        assert len(chained_id_list) == num_messages, "Number of chainedIds should match number of messages"
    
    for i in range(num_messages):
        msg = ParseDict(msg_dict, Message())
        msg.appId = chained_id_list[i]
        msg.id = 1
        msg.user = req.user
        msg.function = req.function
        if input_list is not None:
            serialized_input = serialize_map(input_list[i])
            msg.inputData = bytes(serialized_input)
        msg.chainedId = chained_id_list[i]
        req.messages.append(msg)
    return req