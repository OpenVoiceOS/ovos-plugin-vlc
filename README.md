# VLC OVOS Plugin

The VLC OVOS Plugin integrates VLC media player capabilities with the Open Voice OS (OVOS) ecosystem, providing an audio backend for playing various media formats.

## Features

- Supports playback of various audio formats.
- Provides basic playback controls: play, pause, stop, resume, seek forward, seek backward.
- Volume management with automatic volume adjustments.
- Integration with OVOS for media playback 

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.6 or higher
- VLC media player
- Open Voice OS (OVOS) components


## Configuration

The VLC OVOS Plugin configuration can be set in your `mycroft.conf`

```json
"Audio": {
  "backends": {
    "vlc": {
      "type": "ovos_vlc",
      "active": true,
      "initial_volume": 100,
      "low_volume": 50
    }
  }
}
```

## Usage

The plugin integrates with OVOS to handle audio playback. It supports the following functions:

- **play(repeat=False):** Play the current track.
- **stop():** Stop playback.
- **pause():** Pause playback.
- **resume():** Resume paused playback.
- **lower_volume():** Lower the volume to a predefined level.
- **restore_volume():** Restore the volume to the original level.
- **track_info():** Get information about the current track.
- **get_track_length():** Get the duration of the current track in milliseconds.
- **get_track_position():** Get the current playback position in milliseconds.
- **set_track_position(milliseconds):** Set the playback position in milliseconds.
- **seek_forward(seconds=1):** Seek forward by a specified number of seconds.
- **seek_backward(seconds=1):** Seek backward by a specified number of seconds.


## Troubleshooting

If you encounter any issues, ensure that:
- VLC is correctly installed and accessible.
- The plugin is installed.
- Your configuration file is correctly set up.
- If using containers ensure it is installed in `ovos-audio` container

For further assistance, refer to the official documentation or contact the plugin maintainers.

Check the logs to see what is happening, if specific streams are not playing verify that they play directly in VLC

### Compiling VLC with OpenSSL

youtube streams often fail with errors of the sort

```
[0000758620007870] main tls client error: TLS session handshake timeout
[0000758620007870] main tls client error: connection error: Resource temporarily unavailable
[0000758620007870] gnutls tls client error: TLS handshake error: Error in the push function.
[0000758620007870] main tls client error: TLS session handshake error
[0000758620007870] main tls client error: connection error: Network is unreachable
[0000758620018c40] access stream error: HTTP connection failure
[000075862c1fdeb0] main input error: Your input can't be opened
[000075862c1fdeb0] main input error: VLC is unable to open the MRL 'https://rr1---sn-1vo-v2vd.googlevideo.com/videoplayback?expire=1721262938&ei=-g6YZvHXN7qAmLAP056tuA8&ip=89.154.90.167&id=o-AEGICI_2Jg9Bi7QkLBcrDER2x9Rq0LMgAmp61U3CZP7v&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&mh=uI&mm=31%2C29&mn=sn-1vo-v2vd%2Csn-ovn-apnr&ms=au%2Crdu&mv=m&mvi=1&pl=20&gcr=pt&initcwndbps=1716250&bui=AXc671K3ZtlNAWq5CxbQ_reBYNQZj1xGdH6Gub6fRTySbKLoF7aO7NaO8-iW7yq1xNjANifX1StFFjss&spc=NO7bAVN6YmAuJJ43yqpP5a-HRxHytZ4CnhqOAvQRSv2aVZoiGA2Z9jfjV34W&vprv=1&svpuc=1&mime=audio%2Fwebm&ns=pwlUtDGaUGLlDmo9yJuAleAQ&rqh=1&gir=yes&clen=4016064&dur=256.301&lmt=1714611400333089&mt=1721240936&fvip=1&keepalive=yes&c=WEB&sefc=1&txp=4532434&n=Qaf-nQMDrQNlkw&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cgcr%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AHlkHjAwRgIhANHYmGaXOZBMTCyaTSHguFusnsbtZtqwfgKZPmEpJF7XAiEAlE1d8hD-rlP5uaLzzYVYl7GmJcKujw9fnRlSHcYAq30%3D&sig=AJfQdSswRAIgIciAaSPRUUfi8qN6sd6plEkLD71864lIJlSDLxSv71YCIAcmMv2B5qRWB1cmIXrxEgxm47syThRyc-g3nuiDkcsz'. Check the log for details.
```

recompiling VLC using OpenSSL instead of GnuTLS seems to help

in arch linux this required me to edit the PKGBUILD and make the necessary changes to disable GnuTLS and enable OpenSSL.

Find the configure section and replace:
```
--enable-gnutls
```
with:

```
--disable-gnutls --enable-openssl
```
