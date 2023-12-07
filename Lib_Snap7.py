import snap7
from snap7.types import*
from snap7.util import*



IP = '192.168.3.5'
RACK = 0
SLOT = 1

plc = snap7.client.Client()

# Function read PLC
def ReadMemory(plc, byte, bit, datatype):
      result = plc.read_area(Areas['MK'],0,byte, datatype)
      if datatype == S7WLBit:
            return get_bool(result,0,1)
      elif datatype == S7WLByte or datatype == S7WLWord:
            return get_int(result,0)
      elif datatype == S7WLReal:
            return get_real(result,0)
      elif datatype == S7WLDWord:
            return get_dword(result,0)
      else:
            return None

# Function write PLC
def WriteMemory(plc,byte, bit, datatype, value):
      result = plc.read_area(Areas['MK'],0,byte, datatype)
      if datatype == S7WLBit:
          set_bool(result,0,bit, value)
      elif datatype == S7WLByte or datatype == S7WLWord:
          set_int(result,0, value)
      elif datatype == S7WLReal:
          set_real(result,0, value)
      elif datatype == S7WLDWord:
          set_dword(result,0, value)
      plc.write_area(Areas['MK'],0,byte,result)


plc.connect(IP,RACK,SLOT)
state = plc.get_cpu_state()
plcStatus_get = plc.get_connected()

print(state)
print(plcStatus_get)
