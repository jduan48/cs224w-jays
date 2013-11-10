CORRECT_FILE = 'result/correct';
PREDICTION_FILE = 'result/prediction';

c = load(CORRECT_FILE);
p = load(PREDICTION_FILE);

MAX_LENGTH = 5;
indices = find(c <= MAX_LENGTH & p <= MAX_LENGTH);

x = c(indices, :);
y = p(indices, :);

% change slightly to show all nodes
epi = .3;
clf
hold on
plot(x + rand(size(x, 1), 1) * epi, y + rand(size(y, 1), 1) * epi, 'o')
plot([0 4], [0, 4], 'r');
hold off
