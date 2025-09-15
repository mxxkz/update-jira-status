*** Settings ***
Library           Collections
Library           JSONLibrary
Library           RequestsLibrary
Library           String
Library           ${CURDIR}/ZephyrLibraryUat.py  WITH NAME    ZephyrLibraryUat

*** Variables ***
${WEBHOOK_BASE_URL}    https://script.google.com
${WEBHOOK_PATH}        
${PROJECT}             
${VERSION}             
${CYCLE}               
${FOLDERS_STR}         
@{FOLDERS}             
${ENV}                 

*** Keywords ***
Append To Google Sheet Via Webhook
    [Arguments]    ${results}    ${env}
    ${payload_dict}=    Create Dictionary    results=${results}    env=${env}
    ${payload}=    Evaluate    json.dumps(${payload_dict})    json
    ${headers}=    Create Dictionary    Content-Type=application/json
    Create Session    mysession    ${WEBHOOK_BASE_URL}
    ${response}=    POST On Session    mysession    ${WEBHOOK_PATH}    data=${payload}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    200
    Log    Response: ${response.text}

*** Test Cases ***
Send Executions To Sheet

    ${FOLDERS}=     Set Variable If    '${FOLDERS_STR}' != ""    ${FOLDERS_STR.split(";")}    ${EMPTY}   
    ${results}=    Run Keyword If    '${FOLDERS_STR}' != ""
    ...    ZephyrLibraryUat.Get All Execution Navigation Results    ${PROJECT}    ${VERSION}    ${CYCLE}    ${FOLDERS}
    ...    ELSE        
    ...    ZephyrLibraryUat.Get All Execution Navigation Results    ${PROJECT}    ${VERSION}    ${CYCLE}

    Log     ${results}

    Append To Google Sheet Via Webhook    ${results}    ${ENV}