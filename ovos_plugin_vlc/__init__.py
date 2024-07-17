import time
from typing import List

import vlc
from ovos_bus_client.message import Message
from ovos_plugin_manager.templates.audio import AudioBackend
from ovos_utils.log import LOG


class OVOSVlcService(AudioBackend):
    def __init__(self, config, bus=None, name='ovos_vlc'):
        super(OVOSVlcService, self).__init__(config, bus, name)
        self.config = config
        self.bus = bus
        self.normal_volume = self.config.get('initial_volume', 100)
        self.low_volume = self.config.get('low_volume', 50)
        self._playback_time = 0
        self._last_sync = 0
        self.instance = None
        self.player = None
        self.vlc_events = None
        self.init_vlc()

    def init_vlc(self):
        self.instance = vlc.Instance("--no-video")
        self.player = self.instance.media_player_new()
        self.vlc_events = self.player.event_manager()
        self.vlc_events.event_attach(vlc.EventType.MediaPlayerPlaying,
                                     self.track_start, 1)
        self.vlc_events.event_attach(vlc.EventType.MediaPlayerTimeChanged,
                                     self.update_playback_time, None)
        self.vlc_events.event_attach(vlc.EventType.MediaPlayerEndReached,
                                     self.queue_ended, 0)
        self.vlc_events.event_attach(vlc.EventType.MediaPlayerEncounteredError,
                                     self.handle_vlc_error, None)
        self.vlc_events.event_attach(vlc.EventType.VlmMediaInstanceStatusError,
                                     self.handle_vlc_error, None)
        self.player.audio_set_volume(self.normal_volume)

    ###################
    # vlc internals
    def handle_vlc_error(self, data, other):
        self.ocp_error()

    def update_playback_time(self, data, other):
        self._playback_time = data.u.new_time
        # this message is captured by ovos common play and used to sync the
        # seekbar
        if time.time() - self._last_sync > 2:
            # send event ~ every 2 s
            # the gui seems to lag a lot when sending messages too often,
            # gui expected to keep an internal fake progress bar and sync periodically
            self._last_sync = time.time()
            try:
                self.ocp_sync_playback(self._playback_time)
            except:  # too old OPM version
                self.bus.emit(Message("ovos.common_play.playback_time",
                                      {"position": self._playback_time,
                                       "length": self.get_track_length()}))

    def track_start(self, data, other):
        LOG.debug('VLC playback start')
        if self._track_start_callback:
            self._track_start_callback(self.track_info().get('name', "track"))

    def queue_ended(self, data, other):
        LOG.debug('VLC playback ended')
        self._now_playing = None
        if self._track_start_callback:
            self._track_start_callback(None)

    ############
    # mandatory abstract methods
    @property
    def playback_time(self):
        """ in milliseconds """
        return self._playback_time

    def supported_uris(self) -> List[str]:
        """List of supported uri types.

        Returns:
            list: Supported uri's
        """
        return ['file', 'http', 'https']

    def play(self, repeat=False):
        """ Play playlist using vlc. """
        LOG.debug('VLCService Play')
        # HACK - ensure volume is restored,
        # if stop was called the audio would remain ducked at low volume
        # this is not a proper fix, but it is a good enough remedy
        if self.instance is None or self.player is None:
            self.init_vlc()
        track = self.instance.media_new(self._now_playing)
        self.player.set_media(track)
        self.player.play()

    def stop(self):
        """ Stop vlc playback. """
        LOG.info('VLCService Stop')
        if self.player is not None and self.player.is_playing():
            self.player.stop()
            # HACK - when vlc is stopped it doesnt react properly to commands
            # eg, restore_volume fails. drop the previous reference
            # a new player will be inited on playback request
            self.instance = None
            self.player = None
            self.vlc_events = None
            return True
        return False

    def pause(self):
        """ Pause vlc playback. """
        if self.player is not None:
            self.player.set_pause(1)

    def resume(self):
        """ Resume paused playback. """
        if self.player is not None:
            self.player.set_pause(0)

    def lower_volume(self):
        if self.player is not None:
            current = self.player.audio_get_volume()
            if current <= self.low_volume:
                LOG.info(f"VLC not ducking, volume already below {self.low_volume}")
                return
            LOG.info(f"vlc is volume currently at {current}, lowering to {self.low_volume}")
            self.normal_volume = current  # remember volume
            self.player.audio_set_volume(self.low_volume)

    def restore_volume(self):
        if self.player is not None:
            current = self.player.audio_get_volume()
            if current == self.normal_volume:
                LOG.debug("VLC already at normal volume, ignoring restore_volume request")
                return
            LOG.info(f"restoring vlc volume to {self.normal_volume}")
            for i in range(3):
                self.player.audio_set_volume(self.normal_volume)
                time.sleep(0.2)
                current = self.player.audio_get_volume()
                if current != self.normal_volume:
                    LOG.error("VLC failed to restore volume!")
                else:
                    break

    def track_info(self):
        """ Extract info of current track. """
        ret = {}
        if self.player is not None:
            t = self.player.get_media()
            if t:
                ret['album'] = t.get_meta(vlc.Meta.Album)
                ret['artist'] = t.get_meta(vlc.Meta.Artist)
                ret['title'] = t.get_meta(vlc.Meta.Title)
        return ret

    def get_track_length(self):
        """
        getting the duration of the audio in milliseconds
        """
        if self.player is not None:
            return self.player.get_length()
        return 0

    def get_track_position(self):
        """
        get current position in milliseconds
        """
        if self.player is not None:
            return self.player.get_time()
        return 0

    def set_track_position(self, milliseconds):
        """
        go to position in milliseconds

          Args:
                milliseconds (int): number of milliseconds of final position
        """
        if self.player is not None:
            self.player.set_time(int(milliseconds))

    def seek_forward(self, seconds=1):
        """
        skip X seconds

          Args:
                seconds (int): number of seconds to seek, if negative rewind
        """
        if self.player is not None:
            seconds = seconds * 1000
            new_time = self.player.get_time() + seconds
            duration = self.player.get_length()
            if new_time > duration:
                new_time = duration
            self.player.set_time(new_time)

    def seek_backward(self, seconds=1):
        """
        rewind X seconds

          Args:
                seconds (int): number of seconds to seek, if negative rewind
        """
        if self.player is not None:
            seconds = seconds * 1000
            new_time = self.player.get_time() - seconds
            if new_time < 0:
                new_time = 0
            self.player.set_time(new_time)


def load_service(base_config, bus):
    backends = base_config.get('backends', [])
    services = [(b, backends[b]) for b in backends
                if backends[b]['type'] in ["vlc", 'ovos_vlc'] and
                backends[b].get('active', False)]
    instances = [OVOSVlcService(s[1], bus, s[0]) for s in services]
    return instances


VLCAudioPluginConfig = {
    "vlc": {
        "type": "ovos_vlc",
        "active": True
    }
}
