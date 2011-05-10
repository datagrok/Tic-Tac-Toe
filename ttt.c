#include <stdint.h>
#include <stdio.h>

uint32_t states[0x40000];
uint32_t owins[8];
uint32_t xwins[8] = {
	0b000000000111000000,
	0b000000000000111000,
	0b000000000000000111,
	0b000000000100100100,
	0b000000000010010010,
	0b000000000001001001,
	0b000000000100010001,
	0b000000000001010100,
};

uint32_t valid_state(uint32_t q) {

}

uint32_t whose_turn(uint32_t q) {
	/* Determine the next player to move given a valid board
	 * state. Returns:
	 * 		0: X moves next
	 * 		1: O moves next
	 */
	uint32_t r = 0; /* return value */

	/* Strategy: if the total number of moves (1s) is even, X
	 * moves next. */

	/* Combine the X and O board, mask anything else. */
	q = (q | (q >> 9)) & 0b111111111;

	/* For each occupied space on the board, flip the result. */
	/* FIXME: there is a trick involving (x & (x-1)) that might be useful here.
	 */
	while (q) {
		r = r ^ (q & 1);
		q = q>>1;
	}
	return r;
}

int check_win(uint32_t input) {
	/* Determine if a player has won. Returns:
	 * 		0: X has won
	 * 		1: O has won
	 * 		-1: neither has won
	 */
	int i;
	for (i=0; i<8; i++) {
		if (input & xwins[i] == xwins[i]) {
			return 0;
		}
	}
	return 0;
}

uint32_t next_state(uint32_t input) {

}

void init() {
	int i;
	/* initialize DP work area */
	for (i=0; i<0x40000; i++) {
		states[i] = 0;
	}
	/* initialize win table for O */
	for (i=0; i<8; i++) {
		owins[i] = xwins[i] << 9;
	}
}

void print_state(uint32_t state) {
	char output[13];
	output[3] = output[7] = output[11] = '\n';
	output[12] = '\0';
	int i; /* index */
	for (i=0; i<9; i++) {
		if (state & 1) {
			output[i + i/3] = 'X';
		} else {
			output[i + i/3] = '-';
		}
		state = state>>1;
	}
	for (i=0; i<9; i++) {
		if (state & 1) {
			output[i + i/3] = 'O';
		}
		state = state>>1;
	}
	printf("%s\n", output);
}

int main(int argc, char **argv) {
	int i;
	init();
	for (i=0; i<8; i++) {
		print_state(xwins[i]);
	}
	for (i=0; i<8; i++) {
		print_state(owins[i]);
	}
	return 0;
}
