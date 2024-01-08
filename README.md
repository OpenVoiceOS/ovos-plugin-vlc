# ovos-media-plugin-vlc

vlc plugin for [ovos-media](https://github.com/OpenVoiceOS/ovos-media)

## Install

`pip install ovos-media-plugin-vlc`

## Configuration

```javascript
{
 "media": {

    // keys are the strings defined in "audio_players"
    "preferred_audio_services": ["qt5", "mplayer", "vlc", "cli"],

    // keys are the strings defined in "video_players"
    "preferred_video_services": ["qt5", "mplayer", "vlc", "cli"],

    // PlaybackType.AUDIO handlers
    "audio_players": {
        // vlc player uses a headless vlc instance to handle uris
        "vlc": {
            // the plugin name
            "module": "ovos-media-audio-plugin-vlc",

            // users may request specific handlers in the utterance
            // using these aliases
             "aliases": ["VLC"],

            // deactivate a plugin by setting to false
            "active": true
        }
    },

    // PlaybackType.VIDEO handlers
    "video_players": {
        // vlc player uses a headless vlc instance to handle uris
        "vlc": {
            // the plugin name
            "module": "ovos-media-video-plugin-vlc",

            // users may request specific handlers in the utterance
            // using these aliases
             "aliases": ["VLC"],

            // deactivate a plugin by setting to false
            "active": true
        }
    }
}
```