# Hex and Base64 translator

This script simply translates hexadecimal strings into Base64 strings (by converting them into bits and then reading the bits as Base64) and the inverse process.

The goal of this program is make a password containing only characters in the Base64 alphabet and then being able to split the secret between different parties using [ssss](http://point-at-infinity.org/ssss/) (with the hexadecimal option). With this, an attacker can't get any advantage by discarding unvalid answers, since they are all valid (when running the program normally, you can get "binary" secrets or "ASCII" secrets).

All this trouble is due to the fact that I am not sure if there is a way for an attacker with some shares of the secret to avoid making a brute-force attack by knowing the implementation of ssss and anticipate binary (and therefore invalid) results.

## License

The program is licensed under the GNU General Public License version 3 (available [here](https://www.gnu.org/licenses/gpl-3.0.html)).

## Author

- **Oscar Benedito** - oscar@oscarbenedito.com
