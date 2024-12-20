from langchain_openai import AzureOpenAI  # Import from the updated package

 
# Configuration for Azure OpenAI
api_key = "abc7a61ffc8748e885768d47d6221efe"
azure_endpoint = "https://jnj-ls-rg.openai.azure.com/"  # Use the new azure_endpoint parameter
api_version = "2023-09-15-preview"
deployment_name = "chatbot35"
 
# Define the schema
schema = {
    "pdrmformula": ["FormulaStatus", "FormulaID"],
    "pdrmrawmaterial": ["RawMaterialID", "RawMaterialStatus", "PrimaryFunction"],
    "pdrmrawmaterialformulamapping": ["FormulaID", "RawMaterialID"],
    "pdrmrawmaterialregionmapping": ["Region", "RawMaterialID"],
    "pdrmrawmaterialsuppliercost": ["RawMaterial", "Supplier", "PerKgCost"]
}
 
def get_tables_for_columns(columns):
    """Helper function to determine which tables contain the given columns."""
    tables = set()
    for column in columns:
        for table, cols in schema.items():
            if column in cols:
                tables.add(table)
                break
    return tables
 
def generate_new_trial(input):
    try:
        # Extract requested columns from the input query
        columns = [word.strip(" ,") for word in input.split() if word.strip(" ,") in sum(schema.values(), [])]
        # Determine relevant tables
        relevant_tables = get_tables_for_columns(columns)
        # Prepare the prompt for the language model
        prompt = f"""
        You are a MySQL expert. User asks you questions about the given schema of the database. First, obtain the schema of the database to check the tables, column names, and datatypes, then generate simple MySQL correct queries.
        Here is the database schema:
        -- Table [pdrmformula]
        CREATE TABLE pdrmformula(
            FormulaStatus VARCHAR(50) NULL,
            FormulaID VARCHAR(50) NOT NULL
        );
        -- Table [pdrmrawmaterial]
        CREATE TABLE pdrmrawmaterial(
            RawMaterialID VARCHAR(50) NOT NULL,
            RawMaterialStatus VARCHAR(50) NULL,
            PrimaryFunction VARCHAR(50) NULL,
            PRIMARY KEY (RawMaterialID)
        );
        -- Table [pdrmrawmaterialformulamapping]
        CREATE TABLE pdrmrawmaterialformulamapping(
            FormulaID VARCHAR(50) NOT NULL,
            RawMaterialID VARCHAR(50) NOT NULL
        );
        -- Table [pdrmrawmaterialregionmapping]
        CREATE TABLE pdrmrawmaterialregionmapping(
            Region VARCHAR(50) NULL,
            RawMaterialID VARCHAR(50) NULL
        );
        -- Table [pdrmrawmaterialsuppliercost]
        CREATE TABLE pdrmrawmaterialsuppliercost(
            RawMaterial VARCHAR(500) NULL,
            Supplier VARCHAR(500) NULL,
            PerKgCost DECIMAL(18, 0) NULL
        );
        **User Query:**
        {input}
        **Your Task:**
        1. Translate the natural language query into a corresponding SQL query.
        2. Ensure that the query focuses on finding information based on the raw materials and region specified.
        3. Use the LIKE operator for filters instead of '=' in the WHERE clause (e.g., WHERE XYZ LIKE '%ABC%').
        4. Avoid unnecessary joins. If the requested attributes are present in the same table, do not perform any joins.
        Ensure the SQL query is correctly formatted and syntactically correct.
        """
        # Generate the SQL query using the OpenAI model
        llm = AzureOpenAI(
            deployment_name=deployment_name,
            model_name="text-davinci-003",
            temperature=0.2,
            openai_api_key=api_key,
            azure_endpoint=azure_endpoint,  # Use azure_endpoint instead of openai_api_base
            openai_api_version=api_version,
        )
        response = llm.invoke(prompt)  # Use the 'invoke' method instead of '__call__'
        sql_query = response.strip()  # Adjust based on the actual response format
        
        return sql_query
    except Exception as e:
       
        return None



