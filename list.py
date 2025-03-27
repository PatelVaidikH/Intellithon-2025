import mysql.connector

# Database configuration (Replace with your actual credentials)
db_config = {
    'host': 'localhost',
    'user': 'testuser',
    'password': 'testuser',
    'database': 'intellithon2025'
}

def fetch_unique_locations_and_capabilities():
    """
    Fetch distinct locations and capabilities from MySQL and convert them into Python lists.
    
    Returns:
    tuple: (locations_list, capabilities_list)
    """
    locations_set = set()
    capabilities_set = set()

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch distinct service locations
        cursor.execute("SELECT DISTINCT service_location FROM service_master WHERE service_location IS NOT NULL AND service_location <> ''")
        for row in cursor.fetchall():
            locations_set.add(row[0].strip())

        # Fetch distinct service capabilities
        cursor.execute("SELECT DISTINCT service_capabilities FROM service_master WHERE service_capabilities IS NOT NULL AND service_capabilities <> ''")
        for row in cursor.fetchall():
            # Split comma-separated capabilities into a set
            capabilities = row[0].split(',')
            for capability in capabilities:
                capabilities_set.add(capability.strip())

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    # Convert sets to sorted lists
    return sorted(locations_set), sorted(capabilities_set)

# Fetch and store cleaned lists
locations_list, capabilities_list = fetch_unique_locations_and_capabilities()

# Print the cleaned lists
print("Unique Locations List:")
print(locations_list)

print("\nUnique Capabilities List:")
print(capabilities_list)
