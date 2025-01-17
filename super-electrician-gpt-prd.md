# Electrical Construction Information Assistant
## Product Requirements Document (PRD)
### Version 1.3 - January 2024

## 1. Product Overview

### 1.1 Product Vision
The Electrical Construction Information Assistant is an AI-powered information retrieval system that provides electrical foremen and field personnel with instant access to project documentation through natural language queries. Built and tested on commercial projects, the system addresses the fundamental challenge of accessing scattered technical information across multiple drawing sets, specifications, best practices, and code compliance.

### 1.2 Core Problem Statement
Electrical contractors face unique challenges that this system directly addresses:
- Project information exists across multiple drawing sets (electrical, mechanical, architectural)
- Critical details are scattered through various documents (drawings, specifications, RFIs, submittals)
- Information changes frequently through construction
- Field personnel need immediate access while working
- Electrical work intersects with all trades, requiring comprehensive knowledge access

### 1.3 AI-First Development Approach
The system leverages cutting-edge AI tools throughout its development and operation, including:
- Large Language Models for natural language processing and document understanding
- AI-assisted code development tools for accelerated implementation
- Computer vision models for drawing interpretation
- AI-powered testing and optimization tools

### 1.4 Current Implementation Success
- Deployed and tested on two commercial projects ($300K-$400K range)
- Successfully processes complete drawing sets and specifications
- Enables rapid information retrieval through natural language queries
- Manages version control of project documentation
- Supports multiple concurrent users
- Demonstrates cross-trade information access

## 2. Technical Architecture

### 2.1 Technology Stack
- **AI Processing**: OpenAI's Custom GPTs for natural language understanding
- **Backend Services**: Azure Functions for API integration
- **Search Engine**: Azure AI Search with vector search capabilities
- **Database**: Azure Cosmos DB (MongoDB API) for document storage
- **Processing Pipeline**: Python-based PDF processing with GPT-powered JSON structure conversion
- **Search Implementation**: Python-implemented hybrid search combining Azure Cognitive Search for vectors and keywords
- **Blob Storage**: Azure Blob Storage for storing and retrieving original PDF documents

### 2.2 Data Model Relationships
```
Project
├── Panels
│   ├── Panel Information
│   │   ├── Name (e.g., "21LP-1", "K1S")
│   │   ├── Voltage
│   │   ├── Phases
│   │   └── Specifications
│   └── Circuits
│       ├── Circuit Number
│       ├── Load Description
│       ├── Room Assignments
│       └── Connected Equipment
├── Rooms
│   ├── Room Information
│   │   ├── Room ID
│   │   ├── Room Name
│   │   └── Room Type
│   ├── Electrical Equipment
│   │   ├── Light Fixtures
│   │   ├── Outlets
│   │   └── Special Equipment
│   └── Circuit Assignments
│       ├── Lighting Circuits
│       ├── Power Circuits
│       └── Special Circuits
├── Equipment
│   ├── HVAC Equipment
│   │   ├── Model Information
│   │   ├── Power Requirements
│   │   └── Circuit Assignments
│   ├── Lighting Fixtures
│   │   ├── Fixture Types
│   │   ├── Power Specifications
│   │   └── Control Systems
│   └── Special Systems
│       ├── Fire Alarm
│       ├── Security
│       ├── Building Automation
│       ├── Low-Voltage Data and Voice
│       ├── Low-Voltage Lighting System
│       └── Nurse Call System
├── Plumbing
│   ├── Plumbing Specs
│   └── Plumbing Schedules
└── Architecturals
    ├── Wall Types
    ├── Partition Types
    ├── Ceiling Heights
    ├── Finish Schedule
    └── Floor Plan Dimensions

### 2.3 Database Schema Examples

#### Circuit Collection
```json
{
  "circuit_id": "21LP-1-1",
  "panel": "21LP-1",
  "description": "Lighting",
  "rooms": ["Room_2104", "Room_2105"],
  "equipment": [{
    "type": "Light Fixture",
    "count": 14,
    "model": "F3"
  }]
}
```

#### Room Collection
```json
{
  "room_id": "Room_2104",
  "name": "CONFERENCE 2104",
  "circuits": {
    "lighting": ["21LP-1"],
    "power": ["21LP-17"]
  },
  "equipment": {
    "light_fixtures": [
      {
        "type": "F3",
        "count": 14
      },
      {
        "type": "F4",
        "count": 2
      }
    ],
    "outlets": {
      "regular": 3,
      "controlled": 1
    },
    "data": 4,
    "floor_boxes": 2,
    "switches": {
      "type": "vacancy sensor",
      "model": "WSX-PDT",
      "dimming": "0 to 10V",
      "quantity": 2,
      "mounting_type": "wall-mounted",
      "line_voltage": true
    },
    "fire_devices": [
      {
        "type": "smoke_detector",
        "count": 2
      },
      {
        "type": "pull_station",
        "count": 1
      }
    ]
  },
  "additional_details": {
    "control_system": "Integrated with building automation",
    "installation_date": "March 2023",
    "documentation": "Original installation and circuit diagrams available upon request"
  },
  "electrician_notes": [
    {
      "note": "West Wall not complete, waiting on RFI for chief box location."
    }
  ]
}

### 2.4 Search Implementation Specification

The search implementation uses vector similarity search powered by Azure Cognitive Search and OpenAI embeddings for semantic understanding of electrical code documentation queries.

```python
def nfpa70_search(query: str) -> SearchResults:
    # Generate vector embedding for query
    query_vector = generate_embeddings(query)
    
    # Perform vector similarity search
    vector_results = azure_cognitive_search(
        vector=query_vector,
        k_nearest_neighbors=5
    )
    
    # Process and return results
    return format_search_results(results=vector_results)
```

### Components
- Vector Search: Azure Cognitive Search with OpenAI embeddings
- Code Reference Processing: Extracts NFPA 70 article and section references
- Content Processing: Merges adjacent content and maintains traceability

### TODO: Keyword Search Enhancement
Current implementation uses vector similarity search only. Future enhancement to include keyword search capabilities for improved accuracy and coverage.

## 3. Component Interaction Flow

### 3.1 Example Query Flow
Using a typical query: "What type of fixtures are in Conference Room 232?"

1. User Query → Custom GPT
   - User interacts directly with Custom GPT in OpenAI interface
   - Custom GPT processes query using specialized construction/electrical knowledge
   - Determines appropriate Action to trigger based on query type

2. Custom GPT Action → Azure Function
   - Triggers 'searchDocumentation' Action
   - Constructs HTTP POST request with:
     * Query text
     * Relevant filters (room_number: "232")
   - Sends request to Azure Function endpoint

3. Azure Function → Azure AI Search
   - Converts query into vector embedding using embedding model
   - Constructs search parameters including:
     * Vector representation of query
     * Filters (e.g., room_number="232")
   - Executes search request

4. Azure AI Search → Cosmos DB
   - Performs vector similarity search
   - Applies relevant filters
   - Returns references to matching documents

5. Azure Function → Cosmos DB
   - Retrieves complete document information
   - Gets detailed fixture specifications and metadata

6. Azure Function → Custom GPT → User
   - Returns JSON response matching Action schema
   - Custom GPT formats data into natural language response
   - Presents fixture information to user in conversational format

### 3.2 Component Dependencies
- Custom GPT with defined Actions (OpenAI)
- Azure OpenAI Service
- Azure Functions
- Azure AI Search
- Cosmos DB with MongoDB API
- Azure Document Intelligence (for document processing)

## 4. Core Functionality

### 4.1 Information Access Capabilities
1. **Circuit Information**
   - Circuit assignments and locations
   - Connected equipment details
   - Room assignments
   - Load types and descriptions
   - Original document retrieval for circuit details

2. **Equipment Details**
   - Types of equipment: Light fixtures, outlets, HVAC units, pumps, water heaters, etc.
   - Power requirements
   - Installation specifications
   - Location information
   - Circuit assignments
   - Access to original equipment specification documents

3. **Room-Based Information**
   - Installed devices and fixtures
   - Circuit assignments
   - Special requirements
   - Equipment locations
   - Retrieval of original room layout and specification documents

   *Note: The room-based information is derived from templates that are manually entered. During processing, when a floor plan is recognized, all room numbers are captured. Subsequently, two separate templates are introduced: one for all the electrical information related to that room and another for all the architectural information from that room. Original floor plan documents are also retrievable.*

4. **Cross-Trade Details**
   - HVAC electrical requirements
   - Plumbing system power needs
   - Lighting control systems
   - Building automation interfaces
   - Architectural finish details impacting electrical installs
   - Wall types affecting electrical ring types and electrical routing
   - Ceiling heights for fixture space and electrical routing
   - Concrete and underground work for floor boxes and other installations
   - Access to original cross-trade coordination documents

5. **Architectural Information**
   - Reflected ceiling plan
   - Interior elevations
   - Finish schedule
   - Door details
   - Partition and details
   - General notes
   - Retrieval of original architectural drawings and documents

### 4.2 Key Features
1. **Natural Language Querying**
   - Technical terminology understanding
   - Context-aware responses
   - Follow-up question capability

2. **Document Management**
   - Version tracking
   - Change identification
   - RFI integration
   - Specification updates

3. **Search Capabilities**
   - Vector similarity search
   - Full-text search
   - Hybrid search approaches
   - Relevance ranking

4. **Information Relationships**
   - Cross-reference capability
   - System interconnections
   - Trade coordination details

## 5. Use Cases and Examples

### 5.1 Circuit Investigation
```
User: "What's on circuit 21LP-1?"
System: "Circuit 21LP-1 is a 20A circuit that feeds:
- Lighting for multiple rooms including:
  - Conference Room 2104
  - Room 2105
  - Office 2106
  - Office 2107
  - Office 2108
  - Reception 2137
- Light fixtures include:
  - Type F3 fixtures (total count: 14)
  - Type F4 fixtures (total count: 2)
Connected load details available upon request."
```

### 5.2 Room Equipment Details
```
User: "What electrical equipment is installed in Room 2127 (Server Room)?"
System: "Room 2127 (Server Room) contains:
1. Power Circuits:
   - Circuits 21LP-20, 21LP-24, 21LP-22
2. Equipment:
   - 1x F1 light fixture
   - 2x quad outlets
   - Exhaust fan 2
3. Additional Details:
   - IT equipment connections
   - Dedicated circuits for IT infrastructure
   - Vacancy sensor control (Model: WSX-PDT) with 0-10V dimming"
```

### 5.3 Complex Equipment Query
```
User: "What are the power requirements for AHU-1?"
System: "AHU-1 (Model: LG ARNU543M3A4) specifications:
1. Power Requirements:
   - Voltage: 208/230V-1 phase
   - Circuit: L1-36, 38
   - Protection: 15 amps
2. Physical Specifications:
   - Dimensions: 49-7/32\" x 14-3/16\" x 27-9/16\"
   - Weight: 96.1 lbs
3. Installation Notes:
   - Requires 3#12's wiring
   - Circuit protection: 15 amps"
```

```
User: "What was that job we did in Chicago on the 23rd floor of the Chase building? You remember that one light fixture in the conference room with a dimmable ballast? Can you tell me which circuit it was on and if it was connected to a panel on the floor above?"
System: "The Chicago project on the 23rd floor of the Chase building included:
1. Conference Room Lighting:
   - Fixture: Dimmable ballast type F5
   - Circuit: 23LP-12
   - Panel: Located on the 24th floor, Panel 24LP-1
2. Additional Details:
   - Control System: Integrated with building automation
   - Power Supply: 120V, 20A circuit
   - Installation Date: March 2023
3. Documentation:
   - Original installation and circuit diagrams available upon request."
```

### 5.4 Cross-System Integration
```
User: "Show me the lighting control details for Conference Room 2104"
System: "Conference Room 2104 lighting control setup:
1. Lighting Circuits:
   - Fed from panel 21LP-1
2. Fixtures:
   - 14x Type F3 fixtures
   - 2x Type F4 fixtures
3. Control System:
   - Vacancy sensor type: WSX-PDT
   - Features: 0-10V dimming capability
   - Mounting: Wall-mounted
   - Quantity: 2 sensors
   - Control Type: Line voltage
4. Additional Features:
   - Floor boxes: 2
   - Data connections: 4"
```

### 5.5 Panel Analysis
```
User: "Give me a summary of panel 21LP-1"
System: "Panel 21LP-1 Specifications:
1. Main Details:
   - Voltage: 120/208 Wye
   - Type: MLO (Main Lugs Only)
   - Branch Circuit Breaker Type: Molded Case
   - Mounting: Surface

2. Notable Circuits:
   - Circuit 1: Lighting for multiple rooms
   - Circuits 2/4: EWH-1
   - Circuit 5: Dishwasher
   - Circuits 7-8: Refrigeration equipment
   - Multiple spare circuits available

3. Room Coverage:
   - Serves multiple areas including:
    - Conference rooms
    - Offices
    - Reception area
    - Server room
    - Common areas"
```

## 6. Technical Performance

### 6.1 Current Metrics
- Query response time: < 2 seconds
- Document processing capability: Complete drawing sets
- User support: 20+ concurrent users
- System availability: 99.9%
- Data accuracy: 100% on processed documents

### 6.2 System Capabilities

- **Full Drawing Set Processing**: The system is designed to ingest and process complete sets of construction drawings, ensuring that all relevant plans, including electrical, mechanical, and architectural, are available for query and analysis. This capability allows users to access comprehensive project details without needing to manually sift through multiple documents.

- **Specification Document Handling**: By managing specification documents, the system ensures that all technical requirements and standards are readily accessible. This feature helps in verifying compliance with project specifications and assists in planning and execution by providing detailed technical guidelines.

- **RFI Integration**: The integration of RFIs allows the system to handle formal requests for additional information or clarification. This ensures that all queries and responses are documented and easily retrievable, facilitating clear communication and reducing the risk of misunderstandings during the project lifecycle.

- **Mobile Accessibility**: With mobile accessibility, users can access the system from smartphones or tablets, providing flexibility and convenience. This feature is particularly beneficial for field personnel who need real-time access to information while on-site, enhancing productivity and decision-making.

- **Version Control**: This capability tracks and manages changes to documents and drawings, ensuring that users always have access to the latest versions. It also provides a history of changes, which is crucial for maintaining an accurate record of project evolution and for auditing purposes.

- **Change Tracking**: By monitoring changes to project documents and data, the system provides a clear audit trail. This feature helps in managing updates effectively, ensuring that all stakeholders are aware of modifications and can respond accordingly.

- **Relationship Mapping**: The system identifies and manages the interconnections between different project components and systems. This capability is essential for understanding dependencies and interactions across various trades, facilitating better coordination and planning.

## 7. Value Proposition

### 7.1 Primary Benefits
- Reduces time spent searching for information
- Eliminates need to reference multiple documents
- Provides instant access to critical details
- Ensures accurate information access
- Supports field decision making
- Reduces documentation errors

### 7.2 Secondary Applications
- Training tool for apprentices
- Knowledge base for complex systems
- Project documentation reference
- Installation verification tool
- Field note repository

## 8. Current System Scope

### 8.1 Document Types Processed
- Electrical drawings
- Mechanical drawings
- Plumbing drawings
- Architectural drawings
- Site drawings
- Civil drawings
- Technology drawings (also known as Special Systems or Low Voltage Systems)
- Equipment specifications
- Panel schedules
- RFIs and updates
- Installation requirements

*Note: The specific document types processed can vary from job to job. While electrical, mechanical, plumbing, and architectural drawings are consistently required, other types such as site drawings or civil drawings may not be necessary for certain projects, such as high-rise build-outs where site work is not involved. Additionally, technology drawings may be referred to as Special Systems or Low Voltage Systems, depending on the project.*

### 8.2 Information Types Managed
- Circuit assignments
  - Circuit numbers
  - Load descriptions
  - Room assignments
  - Connected equipment
- Equipment specifications
  - Model information
  - Power requirements
  - Installation guidelines
  - Maintenance schedules
- Room details
  - Room IDs and names
  - Room types and functions
  - Installed devices and fixtures
  - Ceiling heights and finishes
- Installation requirements
  - Step-by-step installation procedures
  - Required tools and materials
  - Safety precautions
  - Code compliance checks
- Cross-trade coordination
  - HVAC electrical requirements
  - Plumbing system power needs
  - Lighting control systems
  - Building automation interfaces
  - Coordination with architectural finishes
  - Architectural details
    - Wall types
    - Ceiling heights
    - Finish schedules
- Technical specifications
  - Detailed technical guidelines
  - Compliance with industry standards
  - Special installation notes
  - Manufacturer recommendations
- Field notes
  - On-site observations
  - Installation deviations
  - Issue tracking and resolutions
  - Keyed notes and annotations
- Code compliance
  - Relevant building codes
  - Electrical standards
  - Inspection requirements
  - Compliance documentation
- Special details
  - Unique project requirements
  - Custom installation instructions
  - Special equipment handling
  - Project-specific notes
