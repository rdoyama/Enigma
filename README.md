## Enigma Machine

This repository contains two main modules: `enigma.py` and `crack.py`, intended to encrypt/decrypt text and find the optimal machine configuration to decrypt a message, respectively. The last module is still under development, so do not expect correct results. This implementation supports both Enigma M3 and M4 "Shark" variations.

### Usage and Documentation

The code is pretty straightforward. As the second module is still incomplete, the following example only covers the encryption/decryption of a simple message. If you want to understand the code and its arguments in detail, use the documentation provided by the Python `help` function and the source code.

```python
>> from enigma import Enigma

>> enigma = Enigma(plugboard="bq cr di ej kw mt os px uz gh",
		   rotors=["Gamma", "V", "II", "III"],
		   reflector="B_thin",
		   offsets="GKDT",
		   rings="HAAA")
>> print(enigma)
Enigma M4 Shark
    - Rotors (left -> right): GAMMA, V, II, III
    - Reflector: B_thin
    - Initial Rotor Settings: GKDT
    - Plugboard: KW CR MT EJ DI GH UZ PX OS BQ
    - Ring Configuration: HAAA

>> enigma.encrypt("This is a Python implementation for the Enigma Machine")
'OYMHWKTKUIAJCKNBKWQQSCGCPTZZVJGPGQJVBRSFPOYEEO'

>> enigma.reset()
>> enigma.decrypt("OYMHWKTKUIAJCKNBKWQQSCGCPTZZVJGPGQJVBRSFPOYEEO")
'THISISAPYTHONIMPLEMENTATIONFORTHEENIGMAMACHINE'
```
