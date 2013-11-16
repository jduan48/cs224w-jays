FILENAME = 'stats/conversation_length_histogram';
A = load(FILENAME);
B = tabulate(A)

B(1:10, :)
C = sum(B(11:end, :))