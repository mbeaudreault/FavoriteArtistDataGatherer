import spotipy
import statistics as stats
from spotipy.oauth2 import SpotifyClientCredentials


class Analyzer:
    """
    @brief Takes user music input prints data about music
    """
    def __init__(self):
        """
        @brief creates a new class
        """
        # Spotipy api
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.user_input = None
        self.user_choices = []
        self.limit_returned = 10
        self.get_and_set_user_input_type()

        if self.user_input == 'song':
            self.get_users_favorite_songs()
        elif self.user_input == 'artist':
            self.get_users_favorite_artist()
        else:
            raise RuntimeError('Incorrect selection')
            exit(1)

        self.get_data()

    def get_and_set_user_input_type(self):
        """
        @brief Get user input for program mode, either song or artist
        """
        user_input = input('Would you like to analyze your favorite artist or songs?' +
                            'enter "artist"  for artist, enter "song" for songs:')
        # Takes user input until the user inputs either artist or song
        while user_input != 'artist' and user_input != 'song':
            user_input = input('Please enter either "artist" or "song":')
        self.user_input = user_input

    def get_users_favorite_songs(self):
        """
        @brief Get user input for 5 songs
        """
        # one loop per song
        for i in range(5):
            fav_song_input = input('Enter the name of one of your favorite song:')
            results = self.sp.search(q=fav_song_input, limit=self.limit_returned)
            # If no results are returned from api ask user to choose a new song
            while len(results['tracks']['items']) < 1:
                fav_song_input = input('Song not found please check spelling or enter new song:')
                results = self.sp.search(q=fav_song_input, limit=self.limit_returned)
            # Loops through JSON returned and prints each song
            for idx, track in enumerate(results['tracks']['items']):
                print('index:', str(idx) + ', track name:', track['name'] +
                 ', Main Artist:', track['album']['artists'][0]['name'])
            song_selection_input = input('Enter index of the correct song:')
            selection_options = range(len(results['tracks']['items']))
            selection_options = [str(i) for i in selection_options]
            # Get user input until user selects a possible index from songs returned
            while song_selection_input not in selection_options:
                song_selection_input = input('Invalid entry, Enter index of the correct song:')
            self.user_choices.append(results['tracks']['items'][int(song_selection_input)]['id'])

    def get_users_favorite_artist(self):
        """
        @brief Get usr input for one artist
        """
        fav_artist_input = input('Enter the name of your favorite artist:')
        results = self.sp.search(q=fav_artist_input, limit=self.limit_returned, type='artist')
        # If no results are returned ask user for new input
        while len(results['artists']['items']) < 1:
            fav_artist_input = input('No artist found please check spelling or enter new artist:')
            results = self.sp.search(q=fav_artist_input, limit=self.limit_returned, type='artist')
        # Loops through JSON returned and prints each artist
        for idx, artist in enumerate(results['artists']['items']):
            try:
                print('index:', str(idx) + ', track name:', artist['name'] +
                 ', Photo Url:', artist['images'][0]['url'])
            except IndexError:
                # Handle error where spotify artist has no picture
                print('index:', str(idx) + ', track name:', artist['name'] +
                 ', Photo Url: no availabe photos')
        artist_selection_input = input('Enter index of the correct artist:')
        selection_options = range(len(results['artists']['items']))
        selection_options = [str(i) for i in selection_options]

        # Get user input until user selects a possible index from songs returned
        while artist_selection_input not in selection_options:
            artist_selection_input = input('Invalid entry, Enter index of the correct artist:')

        selected_artist = results['artists']['items'][int(artist_selection_input)]['id']
        top_tracks_res = self.sp.artist_top_tracks(selected_artist)

        # adds artist top 10 most popular tracks to be analyzed
        for idx, track in enumerate(top_tracks_res['tracks']):
            self.user_choices.append(track['id'])

    def get_data(self):
        """
        @brief Get data of songs from user choice and prints to console
        """
        results = self.sp.audio_features(tracks=self.user_choices)
        danceability = []
        energy = []
        loudness = []
        speechiness =[]
        liveness = []
        valence =[]
        tempo = []
        # Loops through tracks and adds values to each music attribute
        for idx, track in enumerate(results):
            danceability.append(track['danceability'])
            energy.append(track['energy'])
            loudness.append(track['loudness'])
            speechiness.append(track['speechiness'])
            liveness.append(track['liveness'])
            valence.append(track['valence'])
            tempo.append(track['tempo'])
        # print the average of all attributes to console
        print('Data represents averages of songs selected:\n' +
              'danceability:', str(stats.mean(danceability)) + '\n' +
              'energy:', str(stats.mean(energy)) + '\n' +
              'loudness:', str(stats.mean(loudness)) + '\n' +
              'speechiness:', str(stats.mean(speechiness)) + '\n' +
              'liveness:', str(stats.mean(liveness)) + '\n' +
              'valence:', str(stats.mean(valence)) + '\n' +
              'tempo:', str(stats.mean(tempo)))


if __name__ == "__main__":
    analyzer = Analyzer()
