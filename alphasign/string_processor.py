"""
Alpha Sign String Processing Module
Based on the C++ implementation, converts human-readable strings to Alpha sign commands.
"""

class AlphaStringProcessor:
    """
    Processes human-readable strings and converts them to Alpha sign binary commands.
    Supports all the string replacements from the original C++ implementation.
    """
    
    # Line position constants
    LINE_MIDDLE = 0
    LINE_TOP = 1
    LINE_BOTTOM = 2
    LINE_FILL = 3
    
    def __init__(self):
        self.current_line = " "  # Default to middle line
        self.pending_text = ""
        self.pending_memory = ""
        
        # Alpha protocol constants
        self.NULL = chr(0)
        self.SOH = chr(1)
        self.STX = chr(2)
        self.ETX = chr(3)
        self.EOT = chr(4)
        self.ESC = chr(27)
        self.NEW_PAGE = chr(0x0c)
        self.NEW_LINE = chr(0x0d)
        
        # Message speeds
        self.SPEED_1 = chr(0x15)
        self.SPEED_2 = chr(0x16)
        self.SPEED_3 = chr(0x17)
        self.SPEED_4 = chr(0x18)
        self.SPEED_5 = chr(0x19)
        self.NO_HOLD = chr(0x09)
        
        # Colors
        self.SET_COLOR = chr(0x1c)
        self.COLOR_RED = self.SET_COLOR + '1'
        self.COLOR_GREEN = self.SET_COLOR + '2'
        self.COLOR_AMBER = self.SET_COLOR + '3'
        self.COLOR_DIM_RED = self.SET_COLOR + '4'
        self.COLOR_DIM_GREEN = self.SET_COLOR + '5'
        self.COLOR_BROWN = self.SET_COLOR + '6'
        self.COLOR_ORANGE = self.SET_COLOR + '7'
        self.COLOR_YELLOW = self.SET_COLOR + '8'
        self.COLOR_RAINBOW1 = self.SET_COLOR + '9'
        self.COLOR_RAINBOW2 = self.SET_COLOR + 'A'
        self.COLOR_MIX = self.SET_COLOR + 'B'
        self.COLOR_AUTO = self.SET_COLOR + 'C'
        
        # Fonts
        self.SET_FONT = chr(0x1a)
        self.FONT_FIVE_STD = self.SET_FONT + '1'
        self.FONT_FIVE_BOLD = self.SET_FONT + '2'
        self.FONT_FIVE_WIDE = self.SET_FONT + chr(0x3b)
        self.FONT_SEVEN_STD = self.SET_FONT + '3'
        self.FONT_SEVEN_BOLD = self.SET_FONT + '4'
        self.FONT_SEVEN_WIDE = self.SET_FONT + chr(0x3c)
        
        # Character spacing
        self.FONT_SPACING_PROPORTIONAL = chr(0x1e) + '0'
        self.FONT_SPACING_FIXED = chr(0x1e) + '1'
        
        # Priority file
        self.PRIORITY_FILE = chr(0x30)
        
    def set_current_line(self, line_opt):
        """Set the current line on which text appears"""
        line_map = {
            self.LINE_MIDDLE: " ",
            self.LINE_TOP: "\"",
            self.LINE_BOTTOM: "&",
            self.LINE_FILL: "0"
        }
        self.current_line = line_map.get(line_opt, " ")
    
    def new_text_file(self):
        """Start a new text file"""
        self.pending_text = ""
        self.set_current_line(self.LINE_MIDDLE)
    
    def add_text(self, text):
        """Add text to the current text file"""
        self.pending_text += self.make_alpha(text)
    
    def finish_text_file(self, label):
        """Finish the text file and return the data to send"""
        mem = len(self.pending_text) + 8  # Allocate extra space
        return f"A{label}{self.pending_text}"
    
    def make_alpha(self, text):
        """
        Convert human-readable string to Alpha sign binary format.
        This is the core function that handles all the string replacements.
        """
        if not isinstance(text, str):
            text = str(text)
        
        # Speed controls
        text = text.replace("<SPEED:1>", chr(21))
        text = text.replace("</SPEED:1>", chr(9))  # Reset to no speed
        text = text.replace("<SPEED:2>", chr(22))
        text = text.replace("</SPEED:2>", chr(9))  # Reset to no speed
        text = text.replace("<SPEED:3>", chr(23))
        text = text.replace("</SPEED:3>", chr(9))  # Reset to no speed
        text = text.replace("<SPEED:4>", chr(24))
        text = text.replace("</SPEED:4>", chr(9))  # Reset to no speed
        text = text.replace("<SPEED:5>", chr(25))
        text = text.replace("</SPEED:5>", chr(9))  # Reset to no speed
        
        # Colors
        text = text.replace("<C:RED>", chr(28) + "1")
        text = text.replace("</C:RED>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:GREEN>", chr(28) + "2")
        text = text.replace("</C:GREEN>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:AMBER>", chr(28) + "3")
        text = text.replace("</C:AMBER>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:DIMRED>", chr(28) + "4")
        text = text.replace("</C:DIMRED>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:DIMGREEN>", chr(28) + "5")
        text = text.replace("</C:DIMGREEN>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:BROWN>", chr(28) + "6")
        text = text.replace("</C:BROWN>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:ORANGE>", chr(28) + "7")
        text = text.replace("</C:ORANGE>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:YELLOW>", chr(28) + "8")
        text = text.replace("</C:YELLOW>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:RAIN1>", chr(28) + "9")
        text = text.replace("</C:RAIN1>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:RAIN2>", chr(28) + "A")
        text = text.replace("</C:RAIN2>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:COLORMIX>", chr(28) + "B")
        text = text.replace("</C:COLORMIX>", chr(28) + "C")  # Reset to auto
        text = text.replace("<C:AUTO>", chr(28) + "C")
        text = text.replace("</C:AUTO>", chr(28) + "C")  # Reset to auto
        
        # Fonts
        text = text.replace("<F:SANS5>", chr(26) + "1")
        text = text.replace("<F:SANS7>", chr(26) + "3")
        text = text.replace("<F:SERIF7>", chr(26) + "5")
        text = text.replace("<F:SERIF16>", chr(26) + "8")
        text = text.replace("<F:SANS16>", chr(26) + "9")
        
        # Wide modes
        text = text.replace("<WIDE:ON>", chr(29) + "01")
        text = text.replace("<WIDE:OFF>", chr(29) + "00")
        text = text.replace("<DWIDE:ON>", chr(29) + "11")
        text = text.replace("<DWIDE:OFF>", chr(29) + "10")
        
        # Fixed width
        text = text.replace("<FIXEDWIDTH:ON>", chr(29) + "41")
        text = text.replace("<FIXEDWIDTH:OFF>", chr(29) + "40")
        text = text.replace("<FIXED:ON>", chr(30) + "1")
        text = text.replace("<FIXED:OFF>", chr(30) + "0")
        
        # Effects
        text = text.replace("<SCROLL>", chr(27) + self.current_line + "a")
        text = text.replace("<HOLD>", chr(27) + self.current_line + "b")
        text = text.replace("<FLASH>", chr(27) + self.current_line + "c")
        text = text.replace("<ROLL:UP>", chr(27) + self.current_line + "e")
        text = text.replace("<ROLL:DOWN>", chr(27) + self.current_line + "f")
        text = text.replace("<ROLL:LEFT>", chr(27) + self.current_line + "g")
        text = text.replace("<ROLL:RIGHT>", chr(27) + self.current_line + "h")
        text = text.replace("<ROLL:IN>", chr(27) + self.current_line + "p")
        text = text.replace("<ROLL:OUT>", chr(27) + self.current_line + "q")
        
        text = text.replace("<WIPE:UP>", chr(27) + self.current_line + "i")
        text = text.replace("<WIPE:DOWN>", chr(27) + self.current_line + "j")
        text = text.replace("<WIPE:LEFT>", chr(27) + self.current_line + "k")
        text = text.replace("<WIPE:RIGHT>", chr(27) + self.current_line + "l")
        text = text.replace("<WIPE:IN>", chr(27) + self.current_line + "r")
        text = text.replace("<WIPE:OUT>", chr(27) + self.current_line + "s")
        
        # Special effects
        text = text.replace("<2LINESCROLLUP>", chr(27) + self.current_line + "m")
        text = text.replace("<AUTO>", chr(27) + self.current_line + "o")
        text = text.replace("<TWINKLE>", chr(27) + self.current_line + "n0")
        text = text.replace("<SPARKLE>", chr(27) + self.current_line + "n1")
        text = text.replace("<SNOW>", chr(27) + self.current_line + "n2")
        text = text.replace("<INTERLOCK>", chr(27) + self.current_line + "n3")
        text = text.replace("<SWITCH>", chr(27) + self.current_line + "n4")
        text = text.replace("<SLIDE>", chr(27) + self.current_line + "n5")
        text = text.replace("<SPRAY>", chr(27) + self.current_line + "n6")
        text = text.replace("<STARBURST>", chr(27) + self.current_line + "n7")
        
        # Animations
        text = text.replace("<ANIM:WELCOME>", chr(27) + self.current_line + "n8")
        text = text.replace("<ANIM:SLOTS>", chr(27) + self.current_line + "n9")
        text = text.replace("<ANIM:THANKYOU>", chr(27) + self.current_line + "nS")
        text = text.replace("<ANIM:NOSMOKING>", chr(27) + self.current_line + "nU")
        text = text.replace("<ANIM:DRINKDRIVE>", chr(27) + self.current_line + "nV")
        text = text.replace("<ANIM:HORSE>", chr(27) + self.current_line + "nW")
        text = text.replace("<ANIM:FIREWORKS>", chr(27) + self.current_line + "nX")
        text = text.replace("<ANIM:TURBOCAR>", chr(27) + self.current_line + "nY")
        text = text.replace("<ANIM:CHERRYBOMB>", chr(27) + self.current_line + "nZ")
        
        # Other special characters
        text = text.replace("<DATE>", chr(11) + "8")
        text = text.replace("<TIME>", chr(19))
        text = text.replace("<NOHOLD>", chr(9))
        text = text.replace("\\p", chr(12))  # Page break
        text = text.replace("\\n", chr(13))  # New line
        text = text.replace("<STRING>", chr(16))  # String reference
        
        # Handle beep commands
        import re
        beep_pattern = r'<BEEP:(\d+)>'
        def replace_beep(match):
            beep_count = int(match.group(1))
            return self.send_beep(beep_count)
        text = re.sub(beep_pattern, replace_beep, text)
        
        # Handle line positioning
        text = text.replace("<LINE:TOP>", "\"")
        text = text.replace("<LINE:MIDDLE>", " ")
        text = text.replace("<LINE:BOTTOM>", "&")
        text = text.replace("<LINE:FILL>", "0")
        
        return text
    
    def make_hex(self, num, length):
        """Create a hex number padded to the desired number of places"""
        hex_str = format(num, 'X')
        return hex_str.zfill(length)
    
    def send_beep(self, beep_count):
        """Generate beep command"""
        return f"E(2022{format(beep_count - 1, 'X')}"
    
    def set_serial_address(self, new_address):
        """Set the serial address of connected LED signs"""
        return f"E7{new_address}"
    
    def set_run_sequence(self, sequence):
        """Set the order of pages to display"""
        return f"E.TU{sequence}"
    
    def set_string(self, label, value):
        """Set a string variable"""
        return f"G{label}{self.make_alpha(value)}"
    
    def allocate_memory(self, label, mem_type, size):
        """Allocate memory on the Alpha sign"""
        s = label
        if mem_type == 1:  # ALPHA_TEXT
            s += "A"  # Type: Text
            s += "L"  # Locked
            s += self.make_hex(size, 4)  # Size in hex
            s += "FF00"  # Start/stop time
        elif mem_type == 2:  # ALPHA_STRING
            s += "B"  # Type: String
            s += "L"  # Locked
            s += self.make_hex(size, 4)  # Size in hex
            s += "0000"  # Placeholder
        return s
    
    def set_time(self, time_obj=None):
        """Set the time on the sign"""
        import datetime
        if time_obj is None:
            time_obj = datetime.datetime.now()
        
        data = "E"  # Special function command
        data += chr(0x20)  # Set time of day command
        data += time_obj.strftime('%H%M')
        return data
    
    def set_weekday(self, day=None):
        """Set the weekday on the sign"""
        import datetime
        if day is None:
            day = datetime.datetime.now().weekday()
        
        data = "E"  # Special function command
        data += chr(0x26)  # Set day of week
        data += chr(day)
        return data
    
    def set_date(self, date_obj=None):
        """Set the current date on the sign"""
        import datetime
        if date_obj is None:
            date_obj = datetime.datetime.now()
        
        data = "E"  # Special function command
        data += chr(0x3b)  # Set date command
        data += date_obj.strftime('%m%d%y')
        return data
    
    def set_time_format(self, ampm=False):
        """Select between 12 hour and 24 hour time formats"""
        data = "E"  # Special function command
        data += chr(0x27)  # Set time format
        data += 'S' if ampm else 'M'
        return data
    
    def set_sound(self, sound_on=False):
        """Turn sound on or off"""
        data = "E"  # Special function command
        data += chr(0x21)  # Sound control
        data += 'FF' if sound_on else '00'
        return data
    
    def soft_reset(self):
        """Soft reset the sign"""
        data = "E"  # Special function command
        data += chr(0x2c)  # Soft reset
        return data
    
    def set_memory_map(self):
        """Set the internal memory map on the sign"""
        data = "E"  # Special function command
        data += chr(0x24)  # Memory configuration
        
        # Create 5 text files A-E, max 256 byte size, run time set as always
        for i in 'ABCDE':
            data += f"{i}AL0100FF00"
        
        # Create 10 string files with labels 1-10 and max 125 byte size
        for i in range(1, 11):
            data += f"{i}BL007D0000"
        
        return data
    
    def read_error_register(self):
        """Read the signs error register"""
        data = "F"  # Read special function
        data += chr(0x2a)  # Read error register
        return data
    
    def read_memory_size(self):
        """Read the memory size from the sign"""
        data = "F"  # Read special function
        data += chr(0x23)  # Read memory size
        return data
    
    def clear_text(self, file_label):
        """Clear a text file"""
        data = "A"  # Write text command
        data += file_label
        return data
    
    def write_text_file(self, file_label, mode, text):
        """Write a message to a TEXT file"""
        # Convert mode to Alpha protocol format
        mode_map = {
            'rotate': 'a',
            'hold': 'b',
            'flash': 'c',
            'roll_up': 'e',
            'roll_down': 'f',
            'roll_left': 'g',
            'roll_right': 'h',
            'wipe_up': 'i',
            'wipe_down': 'j',
            'wipe_left': 'k',
            'wipe_right': 'l',
            'scroll': 'm',
            'automode': 'o',
            'roll_in': 'p',
            'roll_out': 'q',
            'wipe_in': 'r',
            'wipe_out': 's',
            'c_rotate': 't',
            'twinkle': 'n0',
            'sparkle': 'n1',
            'snow': 'n2',
            'interlock': 'n3',
            'switch': 'n4',
            'slide': 'n5',
            'spray': 'n6',
            'starburst': 'n7',
            'welcome': 'n8',
            'slot_machine': 'n9'
        }
        
        mode_code = mode_map.get(mode, 'a')
        
        data = "A"  # Write text command
        data += file_label
        data += self.ESC
        data += self.current_line  # Use current line setting
        data += mode_code
        data += self.escape_text(text)
        return data
    
    def write_string_file(self, file_label, text):
        """Write text to a STRING file"""
        data = "G"  # Write string command
        data += file_label
        data += self.escape_text(text)
        return data
    
    def escape_text(self, text):
        """Convert non-ASCII characters to escaped extended characters"""
        if not text:
            return ""
        
        # Extended character mappings
        extended_chars = {
            'ä': chr(0x08) + chr(0x24),
            'Ä': chr(0x08) + chr(0x2e),
            'ö': chr(0x08) + chr(0x34),
            'Ö': chr(0x08) + chr(0x39),
            'å': chr(0x08) + chr(0x26),
            'Å': chr(0x08) + chr(0x2f)
        }
        
        escaped = text
        for char, replacement in extended_chars.items():
            escaped = escaped.replace(char, replacement)
        
        # Replace any remaining non-ASCII characters with underscore
        result = ""
        for char in escaped:
            if ord(char) > 127:
                result += '_'
            else:
                result += char
        
        return result
    
    def create_packet_header(self, sign_type="Z", address="00"):
        """Create packet header for Alpha protocol"""
        header = ""
        # Five nulls for baud rate detection
        for _ in range(5):
            header += self.NULL
        # Start of header
        header += self.SOH
        # Sign type and address
        header += sign_type + address
        # Start of text
        header += self.STX
        return header
    
    def create_packet_footer(self, data):
        """Create packet footer with checksum"""
        # Calculate checksum
        checksum = 0
        for char in data:
            checksum += ord(char)
        checksum += ord(self.STX) + ord(self.ETX)
        checksum = checksum % 65535
        
        footer = self.ETX + f"{checksum:04X}" + self.EOT
        return footer
    
    def create_complete_packet(self, data, sign_type="Z", address="00"):
        """Create a complete Alpha protocol packet"""
        header = self.create_packet_header(sign_type, address)
        footer = self.create_packet_footer(data)
        return header + data + footer
    
    def generate_tone(self, tone_type, freq=0, duration=5, repeat=0):
        """Generate tone on the sign (0x28)"""
        data = "E"  # Special function command
        data += chr(0x28)  # Generate tone command
        data += tone_type
        if tone_type == chr(0x32):  # Custom tone
            data += f"{freq:02X}{duration:1X}{repeat:1X}"
        return data
    
    def set_run_time_table(self, label, start, stop):
        """Set run time table (0x29)"""
        data = "E"  # Special function command
        data += chr(0x29)  # Set run time table command
        data += label + start + stop
        return data
    
    def display_text_at_xy(self, enabled, x, y, text):
        """Display text at specific XY coordinates (0x2B)"""
        data = "E"  # Special function command
        data += chr(0x2B)  # Display text at XY command
        status = chr(0x2B) if enabled else chr(0x2D)
        file_ref = chr(0x2B)  # Apparently mandatory
        data += f"{status}{file_ref}{x:02d}{y:02d}{text}"
        return data
    
    def set_dimming_register(self, dim, brightness):
        """Set dimming register (0x2F)"""
        data = "E"  # Special function command
        data += chr(0x2F)  # Set dimming register command
        
        # Get index level closest to brightness
        levels = [100, 86, 72, 58, 44]
        level = min(levels, key=lambda x: abs(x - brightness))
        index = levels.index(level)
        
        data += f"{dim:02X}{index:02d}"
        return data
    
    def set_dimming_time(self, start, stop):
        """Set dimming time schedule (0x2F)"""
        data = "E"  # Special function command
        data += chr(0x2F)  # Set dimming time command
        data += f"{start:02X}{stop:02X}"
        return data
