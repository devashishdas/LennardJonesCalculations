import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Define the Gaussian input template
gaussian_template = """%mem=80GB
%CPU=0-39
%GPUCPU=0=0
%nprocshared=40
%chk=he_dimer_{dist:.3f}.chk
# mp2/aug-cc-pvdz counterpoise=2

Helium Dimer Counterpoise Calculation

0 1 0 1 0 1
 He(Fragment=1)    -{half_dist:.8f}    0.00000000    0.00000000
 He(Fragment=2)     {half_dist:.8f}    0.00000000    0.00000000

"""

# Define distances to calculate
# Increased granularity and range to better capture Lennard-Jones potential
distances = np.linspace(2.5, 4.5, 40).tolist() + np.linspace(4.6, 8.0, 20).tolist()

# Function to create input files
def create_input_files(distances, input_dir="inputs"):
    os.makedirs(input_dir, exist_ok=True)
    for dist in distances:
        half_dist = dist / 2
        input_content = gaussian_template.format(dist=dist, half_dist=half_dist)
        input_path = os.path.join(input_dir, f"he_dimer_{dist:.3f}.gjf")
        with open(input_path, "w") as f:
            f.write(input_content)
        print(f"Input file created: {input_path}")

# Function to run Gaussian and extract results
def run_gaussian_and_extract_energies(distances, input_dir="inputs", output_dir="inputs"):
    os.makedirs(output_dir, exist_ok=True)
    energies = []
    for dist in distances:
        input_file = os.path.join(input_dir, f"he_dimer_{dist:.3f}.gjf")
        output_file = os.path.join(output_dir, f"he_dimer_{dist:.3f}.log")
        # Run Gaussian
        subprocess.run(["g16", input_file], check=True)
        # Rename output file
        if os.path.exists(f"he_dimer_{dist:.3f}.log"):
            os.rename(f"he_dimer_{dist:.3f}.log", output_file)
        # Extract energy
        with open(output_file, "r") as f:
            for line in f:
                if "Counterpoise corrected energy" in line:
                    energy = float(line.split()[-1])  # Energy in Hartree
                    energies.append((dist, energy))
                    print(f"Distance: {dist:.3f} Å, Energy: {energy:.8f} Hartree, Energy: {energy*627.509:.8f} kcal/mol")
                    break
    return energies

# Lennard-Jones potential function
def lennard_jones(r, epsilon, sigma):
    return 4 * epsilon * ((sigma / r)**12 - (sigma / r)**6)

# Function to fit and plot Lennard-Jones results
def fit_and_plot_lj(results, output_file="he_dimer_lj_plot.pdf", grid_style="--"):
    # Separate distances and energies
    distances, energies = zip(*results)
    energies = np.array(energies) * 627.509  # Convert Hartree to kcal/mol
    energies = energies - energies[-1]

    # Perform nonlinear fit
    initial_guess = [0.01, 3.5]  # Initial guess for epsilon and sigma
    popt, _ = curve_fit(lennard_jones, distances, energies, p0=initial_guess)
    epsilon, sigma = popt

    # Generate fitted points
    fpoints = np.linspace(min(distances), max(distances), 100)
    fit_energies = lennard_jones(fpoints, epsilon, sigma)

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.scatter(distances, energies, color="blue", label="Computed Energies")
    plt.plot(fpoints, fit_energies, color="red", linestyle="-", label="LJ Fit")
    plt.axhline(0, color="black", linestyle="--", linewidth=0.8, label="Zero Energy Line")  # Zero energy line
    plt.xlabel("Interatomic Distance (Å)", fontsize=14)
    plt.ylabel("Interaction Energy (kcal/mol)", fontsize=14)
    plt.title("Helium Dimer Lennard-Jones Potential Curve", fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle=grid_style, alpha=0.7)

    # Annotate epsilon and sigma
    plt.text(0.5, 0.5, f"Epsilon: {epsilon:.4f} kcal/mol\nSigma: {sigma:.4f} Å",
             transform=plt.gca().transAxes, fontsize=12, color="green")

    # Save the plot
    plt.savefig(output_file, bbox_inches="tight")
    print(f"Lennard-Jones plot saved as {output_file}")

# Main script
if __name__ == "__main__":
    # Step 1: Create input files
    create_input_files(distances)

    # Step 2: Run Gaussian and extract energies
    results = run_gaussian_and_extract_energies(distances)

    # Step 3: Print results
    print("\nResults (Distance in Å, Energy in Hartree):")
    for dist, energy in results:
        print(f"{dist:.3f} Å: {energy:.8f} Hartree")

    # Step 4: Fit and plot Lennard-Jones results
    fit_and_plot_lj(results)

