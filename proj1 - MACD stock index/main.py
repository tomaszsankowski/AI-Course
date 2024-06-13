import numpy as np
import matplotlib.pyplot as plt

# Funkcja gęstości prawdopodobieństwa rozkładu normalnego
def normal_density(x, mean=0, std_dev=1):
    return 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / std_dev)**2)

# Generowanie próbek z rozkładu normalnego za pomocą metody eliminacji
def generate_normal_samples(n):
    samples = []
    while len(samples) < n:
        u1, u2 = np.random.rand(2)
        x_candidate = -5 + np.random.rand() * 10  # Losujemy wartość z zakresu (-5, 5)
        if u2 <= normal_density(x_candidate) / 2.5:
            samples.append(x_candidate)
    return samples

# Wygenerowanie próbek
samples = generate_normal_samples(10000)

# Wykres funkcji gęstości prawdopodobieństwa rozkładu normalnego
x = np.linspace(-5, 5, 1000)
pdf = normal_density(x)
plt.plot(x, pdf, label='PDF rozkładu normalnego', color='blue')

# Wyświetlenie wykresu
plt.hist(samples, bins=50, density=True, alpha=0.5, color='green', label='Histogram próbek z rozkładu normalnego')
plt.xlabel('Wartość próbki')
plt.ylabel('Prawdopodobieństwo')
plt.title('Funkcja gęstości prawdopodobieństwa (PDF) i histogram próbek z rozkładu normalnego')
plt.legend()
plt.grid(True)
plt.show()
