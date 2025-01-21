# Helium Dimer Lennard-Jones Potential Curve

This repository contains a Python script to compute the interaction energy of a helium dimer using Gaussian MP2 calculations and to fit the results to a Lennard-Jones potential curve. The script also generates plots of the computed energies and the fitted potential curve.

## Features
- Generates Gaussian input files for a range of interatomic distances.
- Extracts interaction energies from Gaussian log files.
- Converts energies to kcal/mol and subtracts reference energy for proper fitting.
- Fits the interaction energies to the Lennard-Jones potential function.
- Produces a plot of the potential curve.

## Prerequisites
Ensure the following dependencies are installed:
- Python 3.7+
- Gaussian software (`g16`) installed and accessible in the system's path.
- Python libraries:
  - `numpy`
  - `matplotlib`
  - `scipy`

You can install the required Python packages using:
```bash
pip install numpy matplotlib scipy
```

## Usage
1. Clone this repository:
   ```bash
   git clone https://github.com/devashishdas/LennardJonesCalculations.git
   cd LennardJonesCalculations
   ```

2. Run the script:
   ```bash
   python S0.py
   ```

3. View the generated Lennard-Jones potential plot (`he_dimer_lj_plot.pdf`).

## Generated Plot
![Helium Dimer Lennard-Jones Potential](he_dimer_lj_plot-1.png)

It is near to the experimental values. I will try with CCSD and changing the distances next.
Please suggest improvements. 

## References

- **ε (kcal/mol)**: Estimates range from approximately 0.011 to 0.013 kcal/mol.

- **σ (Å)**: Estimates range from approximately 2.56 to 2.97 Å.

https://pubs.acs.org/doi/10.1021/acs.jpca.1c00012

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

