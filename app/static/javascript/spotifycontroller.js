const token = "BQBVO5ACFSUY1MelZcrK8b9Xxlgjcn5wN5GT4N8Z6LZRsAkY4DFXvp4iD8bli_nE1llqQGicL0IY5kvz6_wbRQTnjBu0r-DPrG_PWqs8o9Aj2WcHHb_aakcOy7I8pf2-_HKPoEIavBqmcuSH0DAM8hecmNyw_64bbdEa"

window.onSpotifyWebPlaybackSDKReady = () => {
  const player = new Spotify.Player({
    name: 'Web Playback SDK Quick Start Player',
    getOAuthToken: cb => { cb(token); }
  });

  // Error handling
  player.addListener('initialization_error', ({ message }) => { console.error(message); });
  player.addListener('authentication_error', ({ message }) => { console.error(message); });
  player.addListener('account_error', ({ message }) => { console.error(message); });
  player.addListener('playback_error', ({ message }) => { console.error(message); });

  // Playback status updates
  player.addListener('player_state_changed', state => { console.log(state); });

  // Ready
  player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id);
  });

  // Connect to the player!
  player.connect();
};