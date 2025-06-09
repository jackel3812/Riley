"""
RILEY - Science Module

This module provides advanced scientific capabilities including:
- Data analysis and visualization
- Scientific modeling and simulation
- Genomic analysis
- Chemical reaction prediction
- Environmental science calculations
"""

import logging
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re
import random
import json

logger = logging.getLogger(__name__)

class ScienceEngine:
    """Advanced scientific analysis and modeling engine."""
    
    def __init__(self):
        """Initialize the science engine."""
        logger.info("Initializing Science Engine")
        self._load_chemical_data()
        self._load_biological_data()
        self._load_environmental_data()
    
    def _load_chemical_data(self):
        """Load chemical element data."""
        self.periodic_table = {
            "H": {"name": "Hydrogen", "atomic_number": 1, "mass": 1.008, "group": 1, "period": 1},
            "He": {"name": "Helium", "atomic_number": 2, "mass": 4.003, "group": 18, "period": 1},
            "Li": {"name": "Lithium", "atomic_number": 3, "mass": 6.94, "group": 1, "period": 2},
            "Be": {"name": "Beryllium", "atomic_number": 4, "mass": 9.012, "group": 2, "period": 2},
            "B": {"name": "Boron", "atomic_number": 5, "mass": 10.81, "group": 13, "period": 2},
            "C": {"name": "Carbon", "atomic_number": 6, "mass": 12.01, "group": 14, "period": 2},
            "N": {"name": "Nitrogen", "atomic_number": 7, "mass": 14.01, "group": 15, "period": 2},
            "O": {"name": "Oxygen", "atomic_number": 8, "mass": 16.00, "group": 16, "period": 2},
            "F": {"name": "Fluorine", "atomic_number": 9, "mass": 19.00, "group": 17, "period": 2},
            "Ne": {"name": "Neon", "atomic_number": 10, "mass": 20.18, "group": 18, "period": 2},
            # Add more elements as needed
        }
        
        # Common chemical reactions
        self.common_reactions = {
            "combustion": {
                "pattern": r"(C\d*H\d*)\s*\+\s*O2",
                "description": "Combustion of hydrocarbons",
                "general_formula": "CxHy + (x + y/4)O2 → xCO2 + (y/2)H2O"
            },
            "acid_base": {
                "pattern": r"(H[A-Z][a-z]*)\s*\+\s*(Na|K|Li|NH4)[A-Z][a-z]*",
                "description": "Acid-base neutralization",
                "general_formula": "HA + BOH → BA + H2O"
            },
            "precipitation": {
                "pattern": r"(Ag|Pb|Ba|Ca)[A-Z][a-z]*\s*\+\s*(Cl|I|SO4|CO3|PO4)",
                "description": "Precipitation reaction",
                "general_formula": "AX + BY → AY + BX (where one product is insoluble)"
            }
        }
    
    def _load_biological_data(self):
        """Load biological data."""
        # DNA codons to amino acids mapping
        self.genetic_code = {
            'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
            'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
            'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
            'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
            'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
            'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
            'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
            'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
            'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
            'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W',
        }
        
        # Amino acid properties
        self.amino_acid_properties = {
            'A': {'name': 'Alanine', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': 1.8},
            'C': {'name': 'Cysteine', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': 2.5},
            'D': {'name': 'Aspartic Acid', 'polarity': 'polar', 'charge': 'negative', 'hydropathy': -3.5},
            'E': {'name': 'Glutamic Acid', 'polarity': 'polar', 'charge': 'negative', 'hydropathy': -3.5},
            'F': {'name': 'Phenylalanine', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': 2.8},
            'G': {'name': 'Glycine', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': -0.4},
            'H': {'name': 'Histidine', 'polarity': 'polar', 'charge': 'positive', 'hydropathy': -3.2},
            'I': {'name': 'Isoleucine', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': 4.5},
            'K': {'name': 'Lysine', 'polarity': 'polar', 'charge': 'positive', 'hydropathy': -3.9},
            'L': {'name': 'Leucine', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': 3.8},
            'M': {'name': 'Methionine', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': 1.9},
            'N': {'name': 'Asparagine', 'polarity': 'polar', 'charge': 'neutral', 'hydropathy': -3.5},
            'P': {'name': 'Proline', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': -1.6},
            'Q': {'name': 'Glutamine', 'polarity': 'polar', 'charge': 'neutral', 'hydropathy': -3.5},
            'R': {'name': 'Arginine', 'polarity': 'polar', 'charge': 'positive', 'hydropathy': -4.5},
            'S': {'name': 'Serine', 'polarity': 'polar', 'charge': 'neutral', 'hydropathy': -0.8},
            'T': {'name': 'Threonine', 'polarity': 'polar', 'charge': 'neutral', 'hydropathy': -0.7},
            'V': {'name': 'Valine', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': 4.2},
            'W': {'name': 'Tryptophan', 'polarity': 'nonpolar', 'charge': 'neutral', 'hydropathy': -0.9},
            'Y': {'name': 'Tyrosine', 'polarity': 'polar', 'charge': 'neutral', 'hydropathy': -1.3},
            '*': {'name': 'Stop Codon', 'polarity': None, 'charge': None, 'hydropathy': None}
        }
    
    def _load_environmental_data(self):
        """Load environmental science data."""
        # Greenhouse gas properties
        self.greenhouse_gases = {
            "CO2": {
                "name": "Carbon Dioxide",
                "molecular_weight": 44.01,
                "lifetime_years": 100,
                "gwp_100yr": 1
            },
            "CH4": {
                "name": "Methane",
                "molecular_weight": 16.04,
                "lifetime_years": 12,
                "gwp_100yr": 28
            },
            "N2O": {
                "name": "Nitrous Oxide",
                "molecular_weight": 44.01,
                "lifetime_years": 114,
                "gwp_100yr": 265
            },
            "CFC-11": {
                "name": "Trichlorofluoromethane",
                "molecular_weight": 137.37,
                "lifetime_years": 45,
                "gwp_100yr": 4750
            },
            "CFC-12": {
                "name": "Dichlorodifluoromethane",
                "molecular_weight": 120.91,
                "lifetime_years": 100,
                "gwp_100yr": 10900
            }
        }
        
        # Common air pollutants
        self.air_pollutants = {
            "PM2.5": {
                "name": "Particulate Matter (<2.5μm)",
                "who_guideline": 5,  # μg/m³ (annual mean)
                "primary_sources": ["Vehicle emissions", "Industrial processes", "Biomass burning"],
                "health_effects": ["Respiratory diseases", "Cardiovascular diseases", "Premature mortality"]
            },
            "PM10": {
                "name": "Particulate Matter (<10μm)",
                "who_guideline": 15,  # μg/m³ (annual mean)
                "primary_sources": ["Road dust", "Construction", "Agriculture"],
                "health_effects": ["Respiratory irritation", "Asthma exacerbation", "Decreased lung function"]
            },
            "O3": {
                "name": "Ozone",
                "who_guideline": 100,  # μg/m³ (8-hour mean)
                "primary_sources": ["Photochemical reactions", "Vehicle emissions", "Industrial emissions"],
                "health_effects": ["Airway inflammation", "Reduced lung function", "Asthma exacerbation"]
            },
            "NO2": {
                "name": "Nitrogen Dioxide",
                "who_guideline": 10,  # μg/m³ (annual mean)
                "primary_sources": ["Vehicle emissions", "Power plants", "Industrial processes"],
                "health_effects": ["Respiratory inflammation", "Reduced lung function", "Increased respiratory infections"]
            },
            "SO2": {
                "name": "Sulfur Dioxide",
                "who_guideline": 40,  # μg/m³ (24-hour mean)
                "primary_sources": ["Fossil fuel combustion", "Industrial processes", "Volcanic activity"],
                "health_effects": ["Respiratory irritation", "Bronchoconstriction", "Cardiovascular effects"]
            }
        }
    
    # Data Analysis Methods
    
    def analyze_scientific_data(self, data, analysis_type="statistical"):
        """Analyze scientific data.
        
        Args:
            data: List or array of numerical data
            analysis_type: Type of analysis to perform (default: "statistical")
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Convert data to numpy array if it's not already
            if not isinstance(data, np.ndarray):
                data = np.array(data, dtype=float)
            
            if analysis_type == "statistical":
                return self._perform_statistical_analysis(data)
            elif analysis_type == "timeseries":
                return self._perform_timeseries_analysis(data)
            elif analysis_type == "spectral":
                return self._perform_spectral_analysis(data)
            elif analysis_type == "clustering":
                return self._perform_clustering_analysis(data)
            else:
                return {"error": f"Unknown analysis type: {analysis_type}"}
                
        except Exception as e:
            logger.error(f"Error analyzing scientific data: {e}")
            return {"error": f"Could not analyze data: {e}"}
    
    def _perform_statistical_analysis(self, data):
        """Perform statistical analysis on data."""
        try:
            # Basic statistics
            statistics = {
                "count": len(data),
                "min": float(np.min(data)),
                "max": float(np.max(data)),
                "range": float(np.max(data) - np.min(data)),
                "sum": float(np.sum(data)),
                "mean": float(np.mean(data)),
                "median": float(np.median(data)),
                "standard_deviation": float(np.std(data)),
                "variance": float(np.var(data))
            }
            
            # Calculate quartiles
            q1 = float(np.percentile(data, 25))
            q3 = float(np.percentile(data, 75))
            iqr = q3 - q1
            
            statistics.update({
                "percentile_25": q1,
                "percentile_50": float(np.percentile(data, 50)),
                "percentile_75": q3,
                "interquartile_range": iqr
            })
            
            # Calculate skewness and kurtosis
            if len(data) > 2:
                skewness = float(((data - np.mean(data)) ** 3).mean() / ((data - np.mean(data)) ** 2).mean() ** 1.5)
                kurtosis = float(((data - np.mean(data)) ** 4).mean() / ((data - np.mean(data)) ** 2).mean() ** 2 - 3)
                statistics.update({
                    "skewness": skewness,
                    "kurtosis": kurtosis
                })
            
            # Create histogram
            hist, bin_edges = np.histogram(data, bins='auto')
            histogram_data = {
                "bin_counts": hist.tolist(),
                "bin_edges": bin_edges.tolist()
            }
            
            # Generate visualization
            plt.figure(figsize=(10, 6))
            plt.hist(data, bins='auto', alpha=0.7, color='skyblue', edgecolor='black')
            plt.title("Data Distribution")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.grid(True, alpha=0.3)
            
            # Add mean and median lines
            plt.axvline(statistics["mean"], color='red', linestyle='dashed', linewidth=1, label=f'Mean: {statistics["mean"]:.2f}')
            plt.axvline(statistics["median"], color='green', linestyle='dashed', linewidth=1, label=f'Median: {statistics["median"]:.2f}')
            plt.legend()
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            histogram_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            # Create box plot
            plt.figure(figsize=(10, 4))
            plt.boxplot(data, vert=False, patch_artist=True)
            plt.title("Box Plot")
            plt.grid(True, alpha=0.3)
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            boxplot_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "statistics": statistics,
                "histogram": histogram_data,
                "visualizations": {
                    "histogram": histogram_viz,
                    "boxplot": boxplot_viz
                },
                "outliers": self._detect_outliers(data)
            }
            
        except Exception as e:
            logger.error(f"Error in statistical analysis: {e}")
            return {"error": f"Statistical analysis failed: {e}"}
    
    def _detect_outliers(self, data):
        """Detect outliers in the data using IQR method."""
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = [float(x) for x in data if x < lower_bound or x > upper_bound]
        outlier_indices = [i for i, x in enumerate(data) if x < lower_bound or x > upper_bound]
        
        return {
            "count": len(outliers),
            "values": outliers[:10] if len(outliers) > 10 else outliers,  # Limit to 10 outliers
            "indices": outlier_indices[:10] if len(outlier_indices) > 10 else outlier_indices,
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound)
        }
    
    def _perform_timeseries_analysis(self, data):
        """Perform time series analysis on data."""
        try:
            # Generate timestamps if none provided
            # Assume data is evenly spaced in time
            n = len(data)
            timestamps = np.arange(n)
            
            # Calculate moving average (window size = 10% of data points or 5, whichever is larger)
            window_size = max(int(n * 0.1), 5)
            window_size = min(window_size, n - 1)  # Ensure window size is smaller than data length
            
            weights = np.ones(window_size) / window_size
            moving_avg = np.convolve(data, weights, mode='valid')
            
            # Calculate rate of change (derivative)
            rate_of_change = np.diff(data)
            
            # Trend analysis
            if n > 2:
                # Linear trend using polyfit
                z = np.polyfit(timestamps, data, 1)
                slope = float(z[0])
                intercept = float(z[1])
                trend_line = slope * timestamps + intercept
                
                # Determine trend direction
                if slope > 0.01:
                    trend_direction = "increasing"
                elif slope < -0.01:
                    trend_direction = "decreasing"
                else:
                    trend_direction = "stable"
                
                trend_analysis = {
                    "slope": slope,
                    "intercept": intercept,
                    "direction": trend_direction,
                    "trend_line": trend_line.tolist()
                }
            else:
                trend_analysis = {"error": "Not enough data points for trend analysis"}
            
            # Check for seasonality (basic)
            seasonality = None
            if n >= 10:
                # Detrend data
                detrended = data - trend_line
                
                # Calculate autocorrelation
                autocorr = []
                for lag in range(1, min(n // 2, 20)):
                    correlation = np.corrcoef(detrended[lag:], detrended[:-lag])[0, 1]
                    autocorr.append(float(correlation))
                
                # Find peaks in autocorrelation
                # Simple peak detection: a point higher than its neighbors
                peaks = []
                for i in range(1, len(autocorr) - 1):
                    if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1] and autocorr[i] > 0.3:
                        peaks.append(i + 1)  # +1 because lag starts at 1
                
                if peaks:
                    seasonality = {
                        "detected": True,
                        "potential_periods": peaks,
                        "autocorrelation": autocorr
                    }
                else:
                    seasonality = {
                        "detected": False,
                        "autocorrelation": autocorr
                    }
            
            # Generate visualization
            plt.figure(figsize=(12, 8))
            
            # Plot original data
            plt.subplot(3, 1, 1)
            plt.plot(timestamps, data, 'b-', label='Original Data')
            if n > 2:
                plt.plot(timestamps, trend_line, 'r--', label=f'Trend (slope: {slope:.4f})')
            plt.title("Time Series Analysis")
            plt.ylabel("Value")
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Plot moving average
            plt.subplot(3, 1, 2)
            ma_timestamps = timestamps[window_size-1:]
            plt.plot(ma_timestamps, moving_avg, 'g-', label=f'Moving Avg (window: {window_size})')
            plt.ylabel("Value")
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Plot rate of change
            plt.subplot(3, 1, 3)
            roc_timestamps = timestamps[1:]
            plt.plot(roc_timestamps, rate_of_change, 'm-', label='Rate of Change')
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.xlabel("Time")
            plt.ylabel("Change")
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            timeseries_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            # If seasonality detected, create another visualization
            seasonality_viz = None
            if seasonality and seasonality["detected"]:
                plt.figure(figsize=(10, 6))
                plt.plot(range(1, len(autocorr) + 1), autocorr, 'b-', label='Autocorrelation')
                plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
                
                # Mark detected peaks
                for peak in peaks:
                    plt.axvline(x=peak, color='r', linestyle='--', alpha=0.5)
                    plt.text(peak, 0.05, f"Period: {peak}", ha='center')
                
                plt.title("Seasonality Analysis - Autocorrelation")
                plt.xlabel("Lag")
                plt.ylabel("Autocorrelation")
                plt.legend()
                plt.grid(True, alpha=0.3)
                
                # Save visualization to base64
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                buffer.seek(0)
                seasonality_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "original_data_length": n,
                "moving_average": {
                    "window_size": window_size,
                    "values": moving_avg.tolist()
                },
                "rate_of_change": {
                    "values": rate_of_change.tolist(),
                    "mean": float(np.mean(rate_of_change)),
                    "std": float(np.std(rate_of_change))
                },
                "trend_analysis": trend_analysis,
                "seasonality_analysis": seasonality,
                "visualizations": {
                    "timeseries": timeseries_viz,
                    "seasonality": seasonality_viz
                }
            }
            
        except Exception as e:
            logger.error(f"Error in timeseries analysis: {e}")
            return {"error": f"Timeseries analysis failed: {e}"}
    
    def _perform_spectral_analysis(self, data):
        """Perform spectral analysis on data."""
        try:
            n = len(data)
            
            # Compute FFT
            fft_values = np.fft.fft(data)
            freqs = np.fft.fftfreq(n)
            
            # Keep only the positive frequencies
            positive_mask = freqs > 0
            freqs = freqs[positive_mask]
            fft_values = fft_values[positive_mask]
            
            # Calculate magnitude spectrum
            magnitude = np.abs(fft_values)
            
            # Calculate phase spectrum
            phase = np.angle(fft_values)
            
            # Calculate power spectrum (|FFT|^2)
            power = magnitude ** 2
            
            # Find dominant frequencies
            dominant_idx = np.argsort(magnitude)[-5:]  # Top 5 frequencies
            dominant_frequencies = [{
                "frequency": float(freqs[idx]),
                "magnitude": float(magnitude[idx]),
                "phase": float(phase[idx]),
                "power": float(power[idx])
            } for idx in dominant_idx]
            
            # Generate visualization
            plt.figure(figsize=(12, 10))
            
            # Plot original signal
            plt.subplot(3, 1, 1)
            plt.plot(np.arange(n), data, 'b-')
            plt.title("Original Signal")
            plt.ylabel("Amplitude")
            plt.grid(True, alpha=0.3)
            
            # Plot magnitude spectrum
            plt.subplot(3, 1, 2)
            plt.plot(freqs, magnitude, 'g-')
            plt.title("Magnitude Spectrum")
            plt.ylabel("Magnitude")
            plt.grid(True, alpha=0.3)
            
            # Plot power spectrum
            plt.subplot(3, 1, 3)
            plt.plot(freqs, power, 'r-')
            plt.title("Power Spectrum")
            plt.xlabel("Frequency")
            plt.ylabel("Power")
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            spectral_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "spectral_data": {
                    "frequencies": freqs.tolist(),
                    "magnitude": magnitude.tolist(),
                    "phase": phase.tolist(),
                    "power": power.tolist()
                },
                "dominant_frequencies": dominant_frequencies,
                "visualizations": {
                    "spectral": spectral_viz
                }
            }
            
        except Exception as e:
            logger.error(f"Error in spectral analysis: {e}")
            return {"error": f"Spectral analysis failed: {e}"}
    
    def _perform_clustering_analysis(self, data):
        """Perform clustering analysis on data."""
        try:
            # For this simplified implementation, we'll only handle 1D and 2D data
            data_array = np.array(data)
            
            if len(data_array.shape) == 1:
                # Convert 1D data to 2D for clustering
                data_2d = np.column_stack((data_array, np.zeros_like(data_array)))
            elif len(data_array.shape) == 2 and data_array.shape[1] == 2:
                # Already 2D data
                data_2d = data_array
            else:
                return {"error": "Clustering analysis requires 1D or 2D data"}
            
            # Simple clustering using k-means
            # Determine number of clusters (simplified approach)
            n = len(data_2d)
            if n < 10:
                k = 2
            elif n < 100:
                k = 3
            else:
                k = 5
            
            # K-means clustering
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=k, random_state=42).fit(data_2d)
            labels = kmeans.labels_
            centers = kmeans.cluster_centers_
            
            # Count items in each cluster
            cluster_counts = {}
            for i in range(k):
                cluster_counts[i] = int(np.sum(labels == i))
            
            # Calculate cluster statistics
            cluster_stats = []
            for i in range(k):
                cluster_data = data_2d[labels == i]
                if len(cluster_data) > 0:
                    stats = {
                        "cluster_id": i,
                        "size": int(len(cluster_data)),
                        "center": [float(x) for x in centers[i]],
                        "mean": [float(np.mean(cluster_data[:, j])) for j in range(cluster_data.shape[1])],
                        "std": [float(np.std(cluster_data[:, j])) for j in range(cluster_data.shape[1])]
                    }
                    cluster_stats.append(stats)
            
            # Generate visualization
            plt.figure(figsize=(10, 8))
            
            # Color map for clusters
            colors = plt.cm.rainbow(np.linspace(0, 1, k))
            
            # Plot data points with cluster colors
            for i in range(k):
                cluster_data = data_2d[labels == i]
                plt.scatter(cluster_data[:, 0], cluster_data[:, 1], s=50, c=[colors[i]], 
                          label=f'Cluster {i} (n={len(cluster_data)})', alpha=0.6)
            
            # Plot cluster centers
            plt.scatter(centers[:, 0], centers[:, 1], s=200, c='black', marker='X', label='Centroids')
            
            plt.title("K-means Clustering")
            plt.xlabel("Dimension 1")
            plt.ylabel("Dimension 2")
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            clustering_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "clustering_method": "K-means",
                "num_clusters": k,
                "cluster_assignments": labels.tolist(),
                "cluster_centers": centers.tolist(),
                "cluster_statistics": cluster_stats,
                "visualizations": {
                    "clustering": clustering_viz
                }
            }
            
        except Exception as e:
            logger.error(f"Error in clustering analysis: {e}")
            return {"error": f"Clustering analysis failed: {e}"}
    
    # Chemistry Methods
    
    def analyze_chemical_reaction(self, reaction_equation):
        """Analyze a chemical reaction equation.
        
        Args:
            reaction_equation: String representation of a chemical reaction
            
        Returns:
            Dictionary with reaction analysis
        """
        try:
            logger.info(f"Analyzing chemical reaction: {reaction_equation}")
            
            # Standardize equation format
            reaction = self._format_reaction_equation(reaction_equation)
            
            # Split reactants and products
            sides = reaction.split("->")
            if len(sides) != 2:
                sides = reaction.split("=")
            if len(sides) != 2:
                sides = reaction.split("→")
            if len(sides) != 2:
                return {"error": "Invalid reaction format. Use A + B -> C + D format."}
            
            reactants_str = sides[0].strip()
            products_str = sides[1].strip()
            
            # Parse reactants and products
            reactants = [r.strip() for r in reactants_str.split("+")]
            products = [p.strip() for p in products_str.split("+")]
            
            # Extract chemical compounds
            parsed_reactants = [self._parse_chemical_compound(r) for r in reactants]
            parsed_products = [self._parse_chemical_compound(p) for p in products]
            
            # Check for reaction type
            reaction_type = self._identify_reaction_type(parsed_reactants, parsed_products, reaction)
            
            # Check if the reaction is balanced
            balance_check = self._check_reaction_balance(parsed_reactants, parsed_products)
            
            # Calculate reaction properties
            properties = self._calculate_reaction_properties(parsed_reactants, parsed_products)
            
            return {
                "original_equation": reaction_equation,
                "formatted_equation": reaction,
                "reactants": parsed_reactants,
                "products": parsed_products,
                "reaction_type": reaction_type,
                "balance_check": balance_check,
                "properties": properties
            }
            
        except Exception as e:
            logger.error(f"Error analyzing chemical reaction: {e}")
            return {"error": f"Could not analyze reaction: {e}"}
    
    def _format_reaction_equation(self, equation):
        """Standardize a chemical reaction equation format."""
        # Replace common reaction arrow types
        equation = equation.replace("=>", "->").replace("⟶", "->").replace("––>", "->")
        equation = equation.replace("<=>", "->").replace("⟷", "->").replace("<->", "->")
        
        # Remove spaces around plus signs
        equation = re.sub(r'\s*\+\s*', ' + ', equation)
        
        # Remove excess whitespace
        equation = ' '.join(equation.split())
        
        return equation
    
    def _parse_chemical_compound(self, compound_str):
        """Parse a chemical compound string into a structured representation."""
        # Extract coefficient if present
        coefficient = 1
        compound = compound_str
        
        # Extract coefficient pattern (e.g., 2H2O, 0.5O2)
        coef_match = re.match(r'^(\d+\.?\d*|\.\d+)\s*([A-Z].*)', compound_str)
        if coef_match:
            coefficient = float(coef_match.group(1))
            compound = coef_match.group(2)
        
        # Extract elements and their counts
        elements = {}
        element_pattern = r'([A-Z][a-z]*)(\d*)'
        matches = re.findall(element_pattern, compound)
        
        for element, count in matches:
            # If count is empty, default to 1
            count = int(count) if count else 1
            
            # Add to elements dictionary
            if element in elements:
                elements[element] += count
            else:
                elements[element] = count
        
        # Calculate molar mass
        molar_mass = 0
        for element, count in elements.items():
            if element in self.periodic_table:
                molar_mass += self.periodic_table[element]["mass"] * count
        
        return {
            "original": compound_str,
            "compound": compound,
            "coefficient": coefficient,
            "elements": elements,
            "molar_mass": molar_mass
        }
    
    def _identify_reaction_type(self, reactants, products, equation):
        """Identify the type of chemical reaction."""
        # Count reactants and products
        num_reactants = len(reactants)
        num_products = len(products)
        
        # Extract elements from reactants and products
        reactant_elements = set()
        for r in reactants:
            for element in r["elements"].keys():
                reactant_elements.add(element)
                
        product_elements = set()
        for p in products:
            for element in p["elements"].keys():
                product_elements.add(element)
        
        # Check reaction types
        reaction_types = []
        
        # Check for combustion (hydrocarbon + O2 -> CO2 + H2O)
        if any("C" in r["elements"] and "H" in r["elements"] for r in reactants) and \
           any("O" in r["elements"] and len(r["elements"]) == 1 for r in reactants) and \
           any("C" in p["elements"] and "O" in p["elements"] and len(p["elements"]) == 2 for p in products) and \
           any("H" in p["elements"] and "O" in p["elements"] and len(p["elements"]) == 2 for p in products):
            reaction_types.append("Combustion")
        
        # Check for synthesis/combination (A + B -> AB)
        if num_reactants > 1 and num_products == 1:
            reaction_types.append("Synthesis/Combination")
        
        # Check for decomposition (AB -> A + B)
        if num_reactants == 1 and num_products > 1:
            reaction_types.append("Decomposition")
        
        # Check for single replacement (A + BC -> AC + B)
        if num_reactants == 2 and num_products == 2 and \
           (len(reactants[0]["elements"]) == 1 or len(reactants[1]["elements"]) == 1) and \
           (len(products[0]["elements"]) == 1 or len(products[1]["elements"]) == 1):
            reaction_types.append("Single Replacement")
        
        # Check for double replacement (AB + CD -> AD + CB)
        if num_reactants == 2 and num_products == 2 and \
           len(reactants[0]["elements"]) == 2 and len(reactants[1]["elements"]) == 2 and \
           len(products[0]["elements"]) == 2 and len(products[1]["elements"]) == 2:
            reaction_types.append("Double Replacement")
        
        # Check for acid-base neutralization (acid + base -> salt + water)
        for pattern, info in self.common_reactions.items():
            if pattern == "acid_base" and re.search(info["pattern"], equation):
                reaction_types.append("Acid-Base Neutralization")
        
        # Check for oxidation-reduction (electron transfer)
        if reaction_types == []:
            # This is a very simplified check
            # A comprehensive approach would calculate oxidation states
            has_oxygen_reactant = any("O" in r["elements"] for r in reactants)
            has_oxygen_product = any("O" in p["elements"] for p in products)
            if has_oxygen_reactant or has_oxygen_product:
                reaction_types.append("Possible Redox (Oxidation-Reduction)")
        
        if not reaction_types:
            reaction_types = ["Undetermined"]
        
        return reaction_types
    
    def _check_reaction_balance(self, reactants, products):
        """Check if a chemical reaction is balanced."""
        # Count elements on both sides
        reactant_elements = {}
        for reactant in reactants:
            coefficient = reactant["coefficient"]
            for element, count in reactant["elements"].items():
                total_count = coefficient * count
                if element in reactant_elements:
                    reactant_elements[element] += total_count
                else:
                    reactant_elements[element] = total_count
        
        product_elements = {}
        for product in products:
            coefficient = product["coefficient"]
            for element, count in product["elements"].items():
                total_count = coefficient * count
                if element in product_elements:
                    product_elements[element] += total_count
                else:
                    product_elements[element] = total_count
        
        # Check if each element is balanced
        is_balanced = True
        imbalanced_elements = []
        
        all_elements = set(list(reactant_elements.keys()) + list(product_elements.keys()))
        for element in all_elements:
            reactant_count = reactant_elements.get(element, 0)
            product_count = product_elements.get(element, 0)
            
            # Allow for small floating point errors
            if abs(reactant_count - product_count) > 0.01:
                is_balanced = False
                imbalanced_elements.append({
                    "element": element,
                    "reactant_count": reactant_count,
                    "product_count": product_count
                })
        
        return {
            "is_balanced": is_balanced,
            "reactant_elements": reactant_elements,
            "product_elements": product_elements,
            "imbalanced_elements": imbalanced_elements
        }
    
    def _calculate_reaction_properties(self, reactants, products):
        """Calculate properties of the chemical reaction."""
        # Calculate total mass of reactants and products
        total_reactant_mass = sum(r["coefficient"] * r["molar_mass"] for r in reactants)
        total_product_mass = sum(p["coefficient"] * p["molar_mass"] for p in products)
        
        # Calculate limiting reagent (simplified approach)
        limiting_reagent = None
        if len(reactants) > 1:
            # This is a very simplified approach
            # A proper approach would calculate moles and use stoichiometry
            limiting_reagent = min(reactants, key=lambda r: r["coefficient"] * r["molar_mass"])["compound"]
        
        # Simplified calculation of reaction yield
        theoretical_yield = total_product_mass  # Simplified
        
        return {
            "total_reactant_mass": total_reactant_mass,
            "total_product_mass": total_product_mass,
            "mass_difference": total_product_mass - total_reactant_mass,
            "is_mass_conserved": abs(total_product_mass - total_reactant_mass) < 0.01,
            "limiting_reagent": limiting_reagent,
            "theoretical_yield": theoretical_yield
        }
    
    # Biological Methods
    
    def analyze_dna_sequence(self, dna_sequence):
        """Analyze a DNA sequence.
        
        Args:
            dna_sequence: String of DNA nucleotides (A, T, G, C)
            
        Returns:
            Dictionary with DNA sequence analysis
        """
        try:
            logger.info(f"Analyzing DNA sequence of length {len(dna_sequence)}")
            
            # Clean the sequence
            dna_sequence = self._clean_dna_sequence(dna_sequence)
            
            # Basic statistics
            sequence_length = len(dna_sequence)
            
            # Count nucleotides
            nucleotide_counts = {
                'A': dna_sequence.count('A'),
                'T': dna_sequence.count('T'),
                'G': dna_sequence.count('G'),
                'C': dna_sequence.count('C')
            }
            
            # Calculate GC content
            gc_count = nucleotide_counts['G'] + nucleotide_counts['C']
            gc_content = gc_count / sequence_length if sequence_length > 0 else 0
            
            # Calculate nucleotide frequency
            nucleotide_frequency = {
                'A': nucleotide_counts['A'] / sequence_length if sequence_length > 0 else 0,
                'T': nucleotide_counts['T'] / sequence_length if sequence_length > 0 else 0,
                'G': nucleotide_counts['G'] / sequence_length if sequence_length > 0 else 0,
                'C': nucleotide_counts['C'] / sequence_length if sequence_length > 0 else 0
            }
            
            # Find open reading frames
            orfs = self._find_open_reading_frames(dna_sequence)
            
            # Translate to protein
            protein_sequences = []
            for orf in orfs[:3]:  # Only process top 3 ORFs
                protein = self._translate_dna_to_protein(orf["sequence"])
                protein_sequences.append({
                    "start_position": orf["start"],
                    "end_position": orf["end"],
                    "protein_sequence": protein
                })
            
            # Analyze amino acid composition of longest protein
            amino_acid_analysis = None
            if protein_sequences:
                longest_protein = max(protein_sequences, key=lambda p: len(p["protein_sequence"]))
                amino_acid_analysis = self._analyze_amino_acid_composition(longest_protein["protein_sequence"])
            
            # Calculate melting temperature (Tm)
            melting_temp = self._calculate_dna_melting_temperature(dna_sequence)
            
            # Generate visualization
            plt.figure(figsize=(12, 8))
            
            # Plot nucleotide distribution
            plt.subplot(2, 1, 1)
            bars = plt.bar(['A', 'T', 'G', 'C'], 
                          [nucleotide_counts['A'], nucleotide_counts['T'], nucleotide_counts['G'], nucleotide_counts['C']],
                          color=['green', 'red', 'orange', 'blue'])
            plt.title("Nucleotide Distribution")
            plt.ylabel("Count")
            
            # Add count labels
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height}', ha='center', va='bottom')
            
            # Plot GC content along the sequence
            plt.subplot(2, 1, 2)
            window_size = min(100, max(10, int(sequence_length / 20)))  # Adaptive window size
            gc_content_windows = []
            
            for i in range(0, sequence_length - window_size + 1):
                window = dna_sequence[i:i+window_size]
                window_gc = (window.count('G') + window.count('C')) / window_size
                gc_content_windows.append(window_gc)
            
            plt.plot(range(len(gc_content_windows)), gc_content_windows, 'b-')
            plt.axhline(y=gc_content, color='r', linestyle='--', label=f'Average GC: {gc_content:.2f}')
            plt.title(f"GC Content (Window Size: {window_size}bp)")
            plt.xlabel("Position")
            plt.ylabel("GC Content")
            plt.legend()
            
            plt.tight_layout()
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            dna_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "sequence_length": sequence_length,
                "nucleotide_counts": nucleotide_counts,
                "nucleotide_frequency": nucleotide_frequency,
                "gc_content": gc_content,
                "melting_temperature": melting_temp,
                "open_reading_frames": orfs[:5],  # Limit to top 5 ORFs
                "protein_translations": protein_sequences,
                "amino_acid_analysis": amino_acid_analysis,
                "visualizations": {
                    "nucleotide_analysis": dna_viz
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing DNA sequence: {e}")
            return {"error": f"Could not analyze DNA sequence: {e}"}
    
    def _clean_dna_sequence(self, sequence):
        """Clean and validate a DNA sequence."""
        # Remove whitespace and convert to uppercase
        sequence = ''.join(sequence.split()).upper()
        
        # Remove any characters that aren't A, T, G, or C
        sequence = ''.join(c for c in sequence if c in "ATGC")
        
        return sequence
    
    def _find_open_reading_frames(self, dna_sequence):
        """Find potential open reading frames in a DNA sequence."""
        orfs = []
        start_codon = "ATG"
        stop_codons = ["TAA", "TAG", "TGA"]
        
        # Search in all three reading frames
        for frame in range(3):
            i = frame
            while i < len(dna_sequence) - 2:
                # Look for start codon
                if dna_sequence[i:i+3] == start_codon:
                    start_pos = i
                    
                    # Look for stop codon
                    j = i + 3
                    while j < len(dna_sequence) - 2:
                        if dna_sequence[j:j+3] in stop_codons:
                            # Found a complete ORF
                            orf_sequence = dna_sequence[start_pos:j+3]
                            
                            # Only consider ORFs longer than 30 nucleotides
                            if len(orf_sequence) >= 30:
                                orfs.append({
                                    "frame": frame + 1,
                                    "start": start_pos,
                                    "end": j + 2,
                                    "length": len(orf_sequence),
                                    "sequence": orf_sequence
                                })
                            
                            i = j + 3
                            break
                        j += 3
                        
                    if j >= len(dna_sequence) - 2:
                        # No stop codon found
                        i += 3
                else:
                    i += 3
        
        # Sort ORFs by length
        orfs.sort(key=lambda x: x["length"], reverse=True)
        
        return orfs
    
    def _translate_dna_to_protein(self, dna_sequence):
        """Translate a DNA sequence to a protein sequence."""
        protein = ""
        
        # Translate each codon
        for i in range(0, len(dna_sequence) - 2, 3):
            codon = dna_sequence[i:i+3]
            if len(codon) == 3:  # Ensure full codon
                amino_acid = self.genetic_code.get(codon, 'X')
                if amino_acid == '*':
                    break  # Stop at stop codon
                protein += amino_acid
        
        return protein
    
    def _analyze_amino_acid_composition(self, protein_sequence):
        """Analyze the amino acid composition of a protein sequence."""
        # Count amino acids
        aa_counts = {}
        for aa in protein_sequence:
            if aa in aa_counts:
                aa_counts[aa] += 1
            else:
                aa_counts[aa] = 1
        
        # Calculate frequency
        total_aa = len(protein_sequence)
        aa_frequency = {aa: count / total_aa for aa, count in aa_counts.items()}
        
        # Categorize amino acids
        categories = {
            "nonpolar": [],
            "polar": [],
            "positive": [],
            "negative": []
        }
        
        for aa, count in aa_counts.items():
            if aa in self.amino_acid_properties:
                prop = self.amino_acid_properties[aa]
                if prop["charge"] == "positive":
                    categories["positive"].append(aa)
                elif prop["charge"] == "negative":
                    categories["negative"].append(aa)
                elif prop["polarity"] == "polar":
                    categories["polar"].append(aa)
                elif prop["polarity"] == "nonpolar":
                    categories["nonpolar"].append(aa)
        
        # Calculate category counts
        category_counts = {
            "nonpolar": sum(aa_counts.get(aa, 0) for aa in categories["nonpolar"]),
            "polar": sum(aa_counts.get(aa, 0) for aa in categories["polar"]),
            "positive": sum(aa_counts.get(aa, 0) for aa in categories["positive"]),
            "negative": sum(aa_counts.get(aa, 0) for aa in categories["negative"])
        }
        
        # Calculate category percentages
        category_percentages = {cat: count / total_aa * 100 for cat, count in category_counts.items()}
        
        return {
            "length": total_aa,
            "amino_acid_counts": aa_counts,
            "amino_acid_frequency": aa_frequency,
            "categories": categories,
            "category_counts": category_counts,
            "category_percentages": category_percentages
        }
    
    def _calculate_dna_melting_temperature(self, dna_sequence):
        """Calculate the melting temperature of a DNA sequence."""
        # Wallace rule (simplified)
        length = len(dna_sequence)
        
        if length < 14:
            # For short sequences: Tm = 2°C(A+T) + 4°C(G+C)
            a_count = dna_sequence.count('A')
            t_count = dna_sequence.count('T')
            g_count = dna_sequence.count('G')
            c_count = dna_sequence.count('C')
            
            tm = 2 * (a_count + t_count) + 4 * (g_count + c_count)
        else:
            # For longer sequences
            gc_content = (dna_sequence.count('G') + dna_sequence.count('C')) / length
            tm = 81.5 + 0.41 * (gc_content * 100) - (500 / length)
            
            # Salt concentration correction (assuming 50mM Na+)
            tm = tm + 16.6 * (math.log10(0.05))
        
        return tm
    
    # Environmental Science Methods
    
    def calculate_carbon_footprint(self, activities):
        """Calculate carbon footprint based on various activities.
        
        Args:
            activities: Dictionary of activities and their quantities
            
        Returns:
            Dictionary with carbon footprint analysis
        """
        try:
            logger.info(f"Calculating carbon footprint for {len(activities)} activities")
            
            # Define emission factors (kg CO2e per unit)
            emission_factors = {
                "electricity_kwh": 0.371,  # kg CO2e per kWh
                "natural_gas_m3": 2.03,    # kg CO2e per cubic meter
                "gasoline_liter": 2.31,    # kg CO2e per liter
                "diesel_liter": 2.67,      # kg CO2e per liter
                "flight_km": 0.121,        # kg CO2e per km (average per passenger)
                "train_km": 0.041,         # kg CO2e per km (average per passenger)
                "bus_km": 0.089,           # kg CO2e per km (average per passenger)
                "meat_kg": 27.0,           # kg CO2e per kg (beef)
                "chicken_kg": 6.9,         # kg CO2e per kg
                "fish_kg": 6.1,            # kg CO2e per kg
                "dairy_kg": 21.0,          # kg CO2e per kg (cheese)
                "vegetables_kg": 2.0,      # kg CO2e per kg
                "fruits_kg": 1.1,          # kg CO2e per kg
                "waste_kg": 0.45,          # kg CO2e per kg (landfill)
                "recycled_waste_kg": 0.1,  # kg CO2e per kg
                "water_m3": 0.344          # kg CO2e per cubic meter
            }
            
            # Calculate emissions for each activity
            emissions = {}
            total_emissions = 0
            
            for activity, quantity in activities.items():
                if activity in emission_factors:
                    activity_emission = quantity * emission_factors[activity]
                    emissions[activity] = activity_emission
                    total_emissions += activity_emission
            
            # Categorize emissions
            categories = {
                "energy": ["electricity_kwh", "natural_gas_m3"],
                "transportation": ["gasoline_liter", "diesel_liter", "flight_km", "train_km", "bus_km"],
                "food": ["meat_kg", "chicken_kg", "fish_kg", "dairy_kg", "vegetables_kg", "fruits_kg"],
                "waste": ["waste_kg", "recycled_waste_kg"],
                "water": ["water_m3"]
            }
            
            category_emissions = {}
            for category, activity_list in categories.items():
                category_total = sum(emissions.get(activity, 0) for activity in activity_list)
                category_emissions[category] = category_total
            
            # Calculate per capita comparison (global average is ~5 tonnes CO2e per year)
            global_average_daily = 5000 / 365  # kg CO2e per day
            percentage_of_global_average = (total_emissions / global_average_daily) * 100
            
            # Generate offset suggestions
            offset_suggestions = self._generate_offset_suggestions(total_emissions)
            
            # Generate visualization
            plt.figure(figsize=(12, 10))
            
            # Plot emissions by activity
            plt.subplot(2, 1, 1)
            activity_names = list(emissions.keys())
            activity_values = list(emissions.values())
            
            # Sort by emission amount
            sorted_indices = np.argsort(activity_values)[::-1]
            sorted_names = [activity_names[i] for i in sorted_indices]
            sorted_values = [activity_values[i] for i in sorted_indices]
            
            # Only show top 10 activities
            if len(sorted_names) > 10:
                sorted_names = sorted_names[:10]
                sorted_values = sorted_values[:10]
            
            # Replace underscores with spaces and capitalize for display
            display_names = [name.replace('_', ' ').title() for name in sorted_names]
            
            plt.barh(display_names, sorted_values)
            plt.title("Carbon Emissions by Activity")
            plt.xlabel("Emissions (kg CO2e)")
            
            # Plot emissions by category
            plt.subplot(2, 1, 2)
            category_names = list(category_emissions.keys())
            category_values = list(category_emissions.values())
            
            # Sort by emission amount
            sorted_indices = np.argsort(category_values)[::-1]
            sorted_cat_names = [category_names[i].title() for i in sorted_indices]
            sorted_cat_values = [category_values[i] for i in sorted_indices]
            
            plt.pie(sorted_cat_values, labels=sorted_cat_names, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title("Carbon Emissions by Category")
            
            plt.tight_layout()
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            footprint_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "total_emissions": total_emissions,
                "emissions_by_activity": emissions,
                "emissions_by_category": category_emissions,
                "comparison": {
                    "global_average_daily": global_average_daily,
                    "percentage_of_global_average": percentage_of_global_average
                },
                "offset_suggestions": offset_suggestions,
                "visualizations": {
                    "footprint": footprint_viz
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating carbon footprint: {e}")
            return {"error": f"Could not calculate carbon footprint: {e}"}
    
    def _generate_offset_suggestions(self, total_emissions):
        """Generate suggestions for offsetting carbon emissions."""
        # Calculate equivalent actions to offset emissions
        trees_planted = total_emissions / 25  # Approx. 25 kg CO2e absorbed per tree per year
        
        # Renewable energy equivalent
        solar_panels_kwh = total_emissions / 0.371  # kWh from emission factor
        solar_panels = solar_panels_kwh / (5 * 365)  # Assuming 5 kWh/day per panel
        
        # Transportation alternatives
        car_km_saved = total_emissions / 0.14  # Approx. 0.14 kg CO2e per km for average car
        flights_avoided = total_emissions / (900 * 0.121)  # Approx. 900 km short flight
        
        # Diet changes
        beef_meals_reduced = total_emissions / 6.75  # Approx. 6.75 kg CO2e per beef meal (250g)
        
        suggestions = [
            f"Plant {trees_planted:.1f} trees to offset these emissions over one year",
            f"Install {solar_panels:.2f} solar panels to offset these emissions",
            f"Avoid driving {car_km_saved:.1f} km in an average car",
            f"Skip {flights_avoided:.2f} short-haul flights",
            f"Reduce consumption by {beef_meals_reduced:.1f} beef-based meals"
        ]
        
        return suggestions
    
    def analyze_air_quality(self, pollutant_concentrations):
        """Analyze air quality based on pollutant concentrations.
        
        Args:
            pollutant_concentrations: Dictionary of pollutants and their concentrations
            
        Returns:
            Dictionary with air quality analysis
        """
        try:
            logger.info(f"Analyzing air quality with {len(pollutant_concentrations)} pollutants")
            
            # Calculate air quality index
            aqi_values = {}
            highest_aqi = 0
            critical_pollutant = None
            
            for pollutant, concentration in pollutant_concentrations.items():
                if pollutant in self.air_pollutants:
                    # Compare with WHO guideline
                    guideline = self.air_pollutants[pollutant]["who_guideline"]
                    ratio = concentration / guideline
                    
                    # Convert to US AQI-like scale (simplified)
                    aqi = 0
                    if ratio <= 0.5:  # Good
                        aqi = ratio * 100
                    elif ratio <= 1:  # Moderate
                        aqi = 50 + (ratio - 0.5) * 100
                    elif ratio <= 2:  # Unhealthy for sensitive groups
                        aqi = 100 + (ratio - 1) * 50
                    elif ratio <= 5:  # Unhealthy
                        aqi = 150 + (ratio - 2) * 50 / 3
                    else:  # Very unhealthy to hazardous
                        aqi = 200 + min((ratio - 5) * 30, 100)
                    
                    aqi_values[pollutant] = aqi
                    
                    if aqi > highest_aqi:
                        highest_aqi = aqi
                        critical_pollutant = pollutant
            
            # Determine overall air quality category
            category = ""
            health_effects = ""
            recommendations = ""
            
            if highest_aqi <= 50:
                category = "Good"
                health_effects = "Air quality is considered satisfactory, and air pollution poses little or no risk."
                recommendations = "Ideal day for outdoor activities."
            elif highest_aqi <= 100:
                category = "Moderate"
                health_effects = "Air quality is acceptable; however, there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution."
                recommendations = "Unusually sensitive people should consider reducing prolonged or heavy exertion."
            elif highest_aqi <= 150:
                category = "Unhealthy for Sensitive Groups"
                health_effects = "Members of sensitive groups may experience health effects. The general public is not likely to be affected."
                recommendations = "People with respiratory or heart disease, the elderly and children should limit prolonged exertion."
            elif highest_aqi <= 200:
                category = "Unhealthy"
                health_effects = "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
                recommendations = "Everyone should limit prolonged outdoor exertion. Sensitive groups should avoid all outdoor activities."
            elif highest_aqi <= 300:
                category = "Very Unhealthy"
                health_effects = "Health warnings of emergency conditions. The entire population is more likely to be affected."
                recommendations = "Everyone should avoid all outdoor activities. Sensitive groups should remain indoors."
            else:
                category = "Hazardous"
                health_effects = "Health alert: everyone may experience more serious health effects."
                recommendations = "Everyone should avoid all outdoor exertion. Consider evacuation to areas with better air quality."
            
            # Compare with WHO guidelines
            guideline_comparisons = {}
            for pollutant, concentration in pollutant_concentrations.items():
                if pollutant in self.air_pollutants:
                    guideline = self.air_pollutants[pollutant]["who_guideline"]
                    ratio = concentration / guideline
                    status = ""
                    
                    if ratio <= 0.5:
                        status = "Well below guideline"
                    elif ratio <= 0.75:
                        status = "Below guideline"
                    elif ratio <= 1:
                        status = "At guideline"
                    elif ratio <= 2:
                        status = "Exceeds guideline"
                    elif ratio <= 5:
                        status = "Greatly exceeds guideline"
                    else:
                        status = "Severely exceeds guideline"
                    
                    guideline_comparisons[pollutant] = {
                        "concentration": concentration,
                        "who_guideline": guideline,
                        "ratio": ratio,
                        "status": status
                    }
            
            # Generate health risk assessment
            health_risks = {}
            for pollutant, concentration in pollutant_concentrations.items():
                if pollutant in self.air_pollutants:
                    health_effects_list = self.air_pollutants[pollutant]["health_effects"]
                    health_risks[pollutant] = {
                        "effects": health_effects_list,
                        "severity": "Low" if aqi_values[pollutant] <= 100 else 
                                   "Moderate" if aqi_values[pollutant] <= 150 else 
                                   "High" if aqi_values[pollutant] <= 200 else 
                                   "Very High"
                    }
            
            # Generate visualization
            plt.figure(figsize=(12, 10))
            
            # Plot AQI values
            plt.subplot(2, 1, 1)
            pollutant_names = list(aqi_values.keys())
            aqi_vals = list(aqi_values.values())
            
            # Create readable labels
            display_names = [name.replace("_", " ").replace(".", "").upper() for name in pollutant_names]
            
            # Set bar colors based on AQI values
            colors = []
            for aqi in aqi_vals:
                if aqi <= 50:
                    colors.append('green')
                elif aqi <= 100:
                    colors.append('yellow')
                elif aqi <= 150:
                    colors.append('orange')
                elif aqi <= 200:
                    colors.append('red')
                elif aqi <= 300:
                    colors.append('purple')
                else:
                    colors.append('maroon')
            
            bars = plt.bar(display_names, aqi_vals, color=colors)
            plt.title("Air Quality Index by Pollutant")
            plt.ylabel("AQI Value")
            plt.axhline(y=50, color='k', linestyle='--', alpha=0.3)
            plt.axhline(y=100, color='k', linestyle='--', alpha=0.3)
            plt.axhline(y=150, color='k', linestyle='--', alpha=0.3)
            plt.axhline(y=200, color='k', linestyle='--', alpha=0.3)
            plt.axhline(y=300, color='k', linestyle='--', alpha=0.3)
            
            # Add AQI category labels
            plt.text(len(display_names) - 0.5, 25, "Good", ha='right')
            plt.text(len(display_names) - 0.5, 75, "Moderate", ha='right')
            plt.text(len(display_names) - 0.5, 125, "Unhealthy for Sensitive Groups", ha='right')
            plt.text(len(display_names) - 0.5, 175, "Unhealthy", ha='right')
            plt.text(len(display_names) - 0.5, 250, "Very Unhealthy", ha='right')
            plt.text(len(display_names) - 0.5, 350, "Hazardous", ha='right')
            
            # Plot comparison with WHO guidelines
            plt.subplot(2, 1, 2)
            pollutants = list(guideline_comparisons.keys())
            ratios = [guideline_comparisons[p]["ratio"] for p in pollutants]
            
            # Create readable labels
            display_names = [name.replace("_", " ").replace(".", "").upper() for name in pollutants]
            
            # Set bar colors based on ratio to WHO guideline
            colors = []
            for ratio in ratios:
                if ratio <= 0.5:
                    colors.append('green')
                elif ratio <= 0.75:
                    colors.append('yellowgreen')
                elif ratio <= 1:
                    colors.append('gold')
                elif ratio <= 2:
                    colors.append('orange')
                elif ratio <= 5:
                    colors.append('red')
                else:
                    colors.append('darkred')
            
            bars = plt.bar(display_names, ratios, color=colors)
            plt.title("Pollutant Concentrations Relative to WHO Guidelines")
            plt.ylabel("Ratio to WHO Guideline")
            plt.axhline(y=1, color='k', linestyle='--', alpha=0.5, label="WHO Guideline")
            plt.legend()
            
            plt.tight_layout()
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            air_quality_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "overall_aqi": highest_aqi,
                "category": category,
                "critical_pollutant": critical_pollutant,
                "health_effects": health_effects,
                "recommendations": recommendations,
                "aqi_values": aqi_values,
                "guideline_comparisons": guideline_comparisons,
                "health_risks": health_risks,
                "visualizations": {
                    "air_quality": air_quality_viz
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing air quality: {e}")
            return {"error": f"Could not analyze air quality: {e}"}
    
    def model_ecosystem(self, species_interactions, initial_populations, time_steps=100):
        """Model a simplified ecosystem based on species interactions.
        
        Args:
            species_interactions: Matrix of species interaction coefficients
            initial_populations: Dictionary of initial population sizes
            time_steps: Number of time steps to simulate
            
        Returns:
            Dictionary with ecosystem model results
        """
        try:
            logger.info(f"Modeling ecosystem with {len(initial_populations)} species over {time_steps} time steps")
            
            # Convert inputs to numpy arrays
            species = list(initial_populations.keys())
            n_species = len(species)
            
            # Create initial population vector
            populations = np.zeros((time_steps + 1, n_species))
            populations[0] = [initial_populations[sp] for sp in species]
            
            # Ensure interaction matrix is correct size
            interaction_matrix = np.zeros((n_species, n_species))
            for i, sp1 in enumerate(species):
                for j, sp2 in enumerate(species):
                    if sp1 in species_interactions and sp2 in species_interactions[sp1]:
                        interaction_matrix[i, j] = species_interactions[sp1][sp2]
            
            # Add carrying capacity and growth rate (simplified)
            carrying_capacity = np.max(populations[0]) * 2
            growth_rates = np.abs(np.diag(interaction_matrix)) + 0.1
            np.fill_diagonal(interaction_matrix, 0)  # Remove diagonal elements
            
            # Run simulation
            for t in range(time_steps):
                for i in range(n_species):
                    # Basic population growth
                    growth = growth_rates[i] * populations[t, i] * (1 - populations[t, i] / carrying_capacity)
                    
                    # Species interactions
                    interactions = sum(interaction_matrix[i, j] * populations[t, j] for j in range(n_species))
                    
                    # Update population
                    new_pop = populations[t, i] + growth + interactions
                    
                    # Ensure population is non-negative
                    populations[t+1, i] = max(0, new_pop)
            
            # Analyze results
            final_populations = {species[i]: float(populations[-1, i]) for i in range(n_species)}
            
            # Calculate population change
            population_change = {
                species[i]: {
                    "initial": float(populations[0, i]),
                    "final": float(populations[-1, i]),
                    "change": float(populations[-1, i] - populations[0, i]),
                    "percent_change": float((populations[-1, i] - populations[0, i]) / populations[0, i] * 100) if populations[0, i] > 0 else 0
                } for i in range(n_species)
            }
            
            # Identify extinctions and explosions
            extinctions = [sp for sp, data in population_change.items() if data["final"] < 1 and data["initial"] > 1]
            explosions = [sp for sp, data in population_change.items() if data["final"] > data["initial"] * 10]
            
            # Stability analysis (simplified)
            variance = {species[i]: float(np.var(populations[time_steps//2:, i])) for i in range(n_species)}
            stability = {species[i]: "Stable" if variance[species[i]] < populations[-1, i] * 0.1 else "Unstable" for i in range(n_species)}
            
            # Generate visualization
            plt.figure(figsize=(12, 8))
            
            # Plot population dynamics
            for i in range(n_species):
                plt.plot(range(time_steps + 1), populations[:, i], label=species[i])
            
            plt.title("Ecosystem Population Dynamics")
            plt.xlabel("Time Steps")
            plt.ylabel("Population Size")
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            ecosystem_viz = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "species": species,
                "initial_populations": {species[i]: float(populations[0, i]) for i in range(n_species)},
                "final_populations": final_populations,
                "population_change": population_change,
                "extinctions": extinctions,
                "explosions": explosions,
                "stability": stability,
                "population_timeseries": {species[i]: populations[:, i].tolist() for i in range(n_species)},
                "visualizations": {
                    "ecosystem": ecosystem_viz
                }
            }
            
        except Exception as e:
            logger.error(f"Error modeling ecosystem: {e}")
            return {"error": f"Could not model ecosystem: {e}"}

# Initialize the science engine
science_engine = ScienceEngine()

def get_science_engine():
    """Get the global science engine instance."""
    global science_engine
    return science_engine