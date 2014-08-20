# This code is distributed under the GNU General Public License (see
# THE_GENERAL_GNU_PUBLIC_LICENSE.txt for extending this information).
# Copyright (C) 2014, the P2PSP team.

import sys
import struct
from splitter_dbs import Splitter_DBS
from color import Color

# Full-cone Nat Set of rules
class Splitter_FNS(Splitter_DBS):
    # {{{

    def print_modulename(self):
        # {{{

        sys.stdout.write(Color.yellow)
        print("Using FNS")
        sys.stdout.write(Color.none)

        # }}}

    def say_goodbye(self, node, sock):
        # {{{

        sock.sendto('G', node)

        # }}}

    def moderate_the_team(self):
        # {{{

        while self.alive:
            # {{{

            message, sender = self.receive_message()

            if len(message) == 2:

                # {{{ The peer complains about a lost chunk.

                # In this situation, the splitter counts the number of
                # complains. If this number exceeds a threshold, the
                # unsupportive peer is expelled from the
                # team.

                lost_chunk_number = self.get_lost_chunk_number(message)
                self.process_lost_chunk(lost_chunk_number, sender)

                # }}}

            else:
                # {{{ The peer wants to leave the team.

                try:
                    if struct.unpack("s", message)[0] == 'G': # <G>oodbye
                        self.process_goodbye(sender)
                except Exception, e:
                    print(e)
                    print(message)

                # }}}

            # }}}

        # }}}

    # }}}
