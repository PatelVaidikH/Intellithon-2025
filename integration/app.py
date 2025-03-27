from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def parse_search_query(query):
    """
    Parse the search query to extract location and capabilities
    
    Parameters:
    query (str): User search query
    
    Returns:
    dict: Dictionary with extracted location and capabilities
    """
    # Initialize search criteria
    criteria = {
        'location': None,
        'capabilities': None,
        'industry': None
    }
    
    # List of common locations
    locations = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
        'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
        'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 
        'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 
        'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 
        'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 
        'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
        'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
        'West Virginia', 'Wisconsin', 'Wyoming', 'Garrett', 'Mexico'
    ]
    
    # Check for location names in the query
    for location in locations:
        if location.lower() in query.lower().split():
            criteria['location'] = location
            break
    
    # Common capabilities to look for
    common_capabilities = [
        '3D Printing', 'Electro-Mechanical Assembly', 'Engineering & Design', 
        'Fabrication', 'Forging', 'Gears', 'Machining', 'Sheet Metal', 
        'Tool Making', 'Die Making', 'Mold Making', 'Welding', 'cylinder blocks', 'chassis', 'Compression Molding', 'Die Casting', 'Blow Molding', 'Electro-Mechanical Assembly', 'Extrusions', 'Injection Molding', 'Investment Casting', 'Machining', 'Printed Circuit Boards', 'Rotational Molding', 'RTV Molding', 'Sand Mold Casting', 'Sheet Metal', 'Stamping', 'Structural Foam Molding', 'Thermoforming', 'Tube Modification', 'Wire Harness', 'Woodworking'
    ]
    
    # Check for capabilities in the query
    for capability in common_capabilities:
        if capability.lower() in query.lower() or capability.lower().replace(' ', '') in query.lower().replace(' ', ''):
            criteria['capabilities'] = capability
            break
    
    # Specific capability checks
    if 'fabrication' in query.lower() or 'fabricate' in query.lower():
        criteria['capabilities'] = 'Fabrication'
    elif '3d print' in query.lower():
        criteria['capabilities'] = '3D Printing'
    elif 'machining' in query.lower() or 'machine' in query.lower():
        criteria['capabilities'] = 'Machining'
    
    return criteria

def search_suppliers_direct(search_criteria, industry_filter=None):
    """
    Search for suppliers that meet ALL the specified criteria (AND logic)
    
    Parameters:
    search_criteria (dict): Dictionary with location and capabilities criteria
    industry_filter (str, optional): Industry to filter by
    
    Returns:
    list: Matching suppliers
    """
    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'testuser',
        'password': 'testuser',
        'database': 'intellithon2025'
    }
    
    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Build SQL query with AND logic for all criteria
        query = """
        SELECT service_id, service_name, details_url, service_location, 
               service_description, service_capabilities, post_tags, service_rating
        FROM intellithon2025.service_master
        WHERE 1=1
        """
        
        params = []
        
        # Add location filter if provided
        if search_criteria['location']:
            query += " AND service_location LIKE %s"
            params.append(f"%{search_criteria['location']}%")
        
        # Add capabilities filter if provided
        if search_criteria['capabilities']:
            query += " AND service_capabilities LIKE %s"
            params.append(f"%{search_criteria['capabilities']}%")
        
        # Add industry filter if provided
        if industry_filter and industry_filter != "":
            query += " AND post_tags LIKE %s"
            params.append(f"%{industry_filter}%")
        
        # Execute query
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Convert decimal and other non-serializable types to strings/primitives for JSON
        for result in results:
            for key, value in result.items():
                if isinstance(value, (bytes, bytearray)):
                    result[key] = value.decode('utf-8')
                # Handle other potential non-serializable types
        
        return results
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/search', methods=['POST'])
def search_api():
    data = request.json
    search_query = data.get('searchQuery', '')
    industry_filter = data.get('industryFilter', '')
    
    # Extract search criteria from query
    search_criteria = parse_search_query(search_query)
    
    # Search suppliers
    results = search_suppliers_direct(search_criteria, industry_filter)
    
    return jsonify({
        'results': results,
        'count': len(results),
        'criteria': search_criteria
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)