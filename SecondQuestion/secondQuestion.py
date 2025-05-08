import os
import glob
import csv
from collections import defaultdict

def analyze_temperature_data():
    """
    Analyzes temperature data from multiple weather stations across different years.
    Processes CSV files containing monthly temperature data and produces:
    - Seasonal averages for each station
    - Overall seasonal averages
    - Stations with largest temperature ranges
    - Warmest and coolest stations
    """
    
    # Define seasons for Southern Hemisphere (Australia)
    seasons = {
        'Summer': ['December', 'January', 'February'],
        'Autumn': ['March', 'April', 'May'],
        'Winter': ['June', 'July', 'August'],
        'Spring': ['September', 'October', 'November']
    }
    
    # Initialize data structures:
    # seasonal_temps: Nested dictionary to store temperatures by season and station
    # station_ranges: Stores temperature ranges for each station
    # station_annual_avgs: Stores annual averages for each station
    seasonal_temps = defaultdict(lambda: defaultdict(list))  # season -> station -> [temps]
    station_ranges = {}  # station -> [ranges]
    station_annual_avgs = defaultdict(list)  # station -> [annual averages]
    
    # Find all CSV files in the temperatures folder matching the pattern
    csv_files = glob.glob(os.path.join('temperatures', 'stations_group_*.csv'))
    
    # Process each year's data file
    for file_path in csv_files:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Process each row (station) in the CSV file
            for row in reader:
                station_name = row['STATION_NAME']
                monthly_temps = {}  # Temporary storage for this station's monthly temps
                
                # Extract and convert monthly temperature values
                for month in ['January', 'February', 'March', 'April', 'May', 'June',
                             'July', 'August', 'September', 'October', 'November', 'December']:
                    try:
                        monthly_temps[month] = float(row[month])
                    except ValueError:
                        # Handle missing or invalid data (though sample data is complete)
                        monthly_temps[month] = None
                
                # Calculate annual average temperature (excluding missing data)
                valid_temps = [t for t in monthly_temps.values() if t is not None]
                if valid_temps:
                    annual_avg = sum(valid_temps) / len(valid_temps)
                    station_annual_avgs[station_name].append(annual_avg)
                
                # Calculate temperature range for this year
                valid_temps = [t for t in monthly_temps.values() if t is not None]
                if valid_temps:
                    temp_range = max(valid_temps) - min(valid_temps)
                    if station_name in station_ranges:
                        station_ranges[station_name].append(temp_range)
                    else:
                        station_ranges[station_name] = [temp_range]
                
                # Organize temperatures by season for seasonal analysis
                for season, months in seasons.items():
                    season_temps = [monthly_temps[month] for month in months 
                                  if monthly_temps[month] is not None]
                    if season_temps:
                        seasonal_temps[season][station_name].extend(season_temps)
    
    # Calculate average temperatures for each season at each station
    seasonal_averages = {}
    for season in seasons:
        season_avg = {}
        for station, temps in seasonal_temps[season].items():
            season_avg[station] = sum(temps) / len(temps)
        seasonal_averages[season] = season_avg
    
    # Calculate overall seasonal averages across all stations
    overall_seasonal_avgs = {}
    for season in seasons:
        all_temps = []
        for station_temps in seasonal_temps[season].values():
            all_temps.extend(station_temps)
        overall_seasonal_avgs[season] = sum(all_temps) / len(all_temps) if all_temps else None
    
    # Find station(s) with largest average temperature range
    avg_ranges = {station: sum(ranges)/len(ranges) for station, ranges in station_ranges.items()}
    max_range = max(avg_ranges.values())
    max_range_stations = [station for station, r in avg_ranges.items() if r == max_range]
    
    # Find warmest and coolest stations based on annual averages
    avg_annual_temps = {station: sum(temps)/len(temps) for station, temps in station_annual_avgs.items()}
    max_temp = max(avg_annual_temps.values())
    min_temp = min(avg_annual_temps.values())
    warmest_stations = [station for station, t in avg_annual_temps.items() if t == max_temp]
    coolest_stations = [station for station, t in avg_annual_temps.items() if t == min_temp]
    
    # Write analysis results to output files
    
    # File 1: Average temperatures by season (overall and per station)
    with open('average_temp.txt', 'w') as f:
        f.write("Average Temperatures by Season (across all stations and years):\n")
        for season, temp in overall_seasonal_avgs.items():
            f.write(f"{season}: {temp:.2f}°C\n")
        
        f.write("\nDetailed Averages by Station:\n")
        for season in seasons:
            f.write(f"\n{season}:\n")
            for station, temp in seasonal_averages[season].items():
                f.write(f"{station}: {temp:.2f}°C\n")
    
    # File 2: Stations with largest temperature ranges
    with open('largest_temp_range_station.txt', 'w') as f:
        f.write("Station(s) with the largest temperature range:\n")
        for station in max_range_stations:
            f.write(f"{station}: {avg_ranges[station]:.2f}°C range\n")
    
    # File 3: Warmest and coolest stations
    with open('warmest_and_coolest_station.txt', 'w') as f:
        f.write("Warmest Station(s):\n")
        for station in warmest_stations:
            f.write(f"{station}: {avg_annual_temps[station]:.2f}°C\n")
        
        f.write("\nCoolest Station(s):\n")
        for station in coolest_stations:
            f.write(f"{station}: {avg_annual_temps[station]:.2f}°C\n")
    
    # Print completion message with output file names
    print("Analysis complete. Results saved to:")
    print("- average_temp.txt")
    print("- largest_temp_range_station.txt")
    print("- warmest_and_coolest_station.txt")

if __name__ == "__main__":
    analyze_temperature_data()