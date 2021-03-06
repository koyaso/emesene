import songretriever
import DBusBase

# Handler for players that follow the mpris spec
# See: http://xmms2.org/wiki/Media_Player_Interfaces

class MprisMusicHandlerConfig(songretriever.BaseMusicHandlerConfig):
    '''the panel to display/modify the config related to
    the 'listening to' extension for the MPRIS music handler'''

    def __init__(self):
        '''constructor'''
        songretriever. BaseMusicHandlerConfig.__init__(self)

        self.player_default = "Audacious"
        # This should be loaded from a config option
        self.player = self.player_default
        self.append_entry_default('Player', 'player', self.player_default)


class MprisHandler(DBusBase.DBusBase):
    '''Handler for players that follow the MPRIS specification'''
    NAME = 'MPRIS'
    DESCRIPTION = 'Music handler for MPRIS players'
    AUTHOR = 'Karasu'
    WEBSITE = 'www.emesene.org'

    def __init__(self, main_window = None,
                 iface_name = 'org.mpris.amarok',
                 iface_path = '/TrackList'):
        DBusBase.DBusBase.__init__(self, main_window, iface_name, iface_path)

        # Use our specific config dialog
        self.config = MprisMusicHandlerConfig()

    def is_playing(self):
        '''Returns True if a song is being played'''
        if self.is_running():
            is_playing_iface = self.bus.get_object(self.iface_name, '/Player')
            if is_playing_iface:
                status = is_playing_iface.GetStatus()
                if status[0] == 0:
                    return True
        return False

    def get_current_song(self):
        '''Returns the current song in the correct format'''
        if self.is_playing():
            track = self.iface.GetCurrentTrack()
            song = self.iface.GetMetadata(track)
            return songretriever.Song(song['artist'],
                                      song['album'],
                                      song['title'],
                                      song['location'])

