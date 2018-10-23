# freshdesk 
  https://freshdesk.com/
  
### Overview  

Freshdesk is an award-winning cloud-hosted help desk solution with useful features. Freshdesk is designed to meet the demands of both small businesses and large companies. The solution also includes standard features, such as, help desk ticketing, knowledge base, and community platform. Once set up, Freshdesk turns your support emails into tickets that you can be track for rapid and accurate responses. 

##### PRE-REQUISITES to use freshdesk and DNIF  
Outbound access required for github to clone the plugin

| Protocol   | Source IP  | Source Port  | Direction	 | Destination Domain | Destination Port  |  
|:------------- |:-------------|:-------------|:-------------|:-------------|:-------------|  
| TCP | DS,CR,A10 | Any | Egress	| github.com | 443 | 
| TCP | DS,CR,A10 | Any | Egress	| freshdesk.com | 443 |

 
## freshdesk trigger plugin functions
Details of the function that can be used with the freshdesk trigger is given in this section.

### create_ticket 
This function allows for creating a ticket against an observerd event using the defined (custom/default template)  .

### Input  
- Subject of ticket.(Note Commas(,) cannot be used as they are used for Input parameters seperation ) 
- Event Field prenset in the event .
- Template name to be triggered.(Note if this field is not provided the default template gets triggered)   

### Example
```
_fetch * from event where $Action = LOGIN_FAIL AND $Duration=30d limit 1
>>_trigger api freshdesk create_ticket Login Fail observed for user : , $User , default.txt
```

### Output  

Click [here](https://drive.google.com/file/d/15J85kxayh96-_UAORrdRf8MHlEUClqL4/view?usp=sharing) to view the output of the above example.

![freshdesk](https://user-images.githubusercontent.com/37173181/47280578-b7f7b180-d5f4-11e8-9320-1f1e4f577629.jpg)

The trigger call returns output in the following structure for available data

  | Fields        | Description  |
|:------------- |:-------------|
| $FDCreatedAt  | Ticket creation timestamp |
| $FDDescription | HTML content of the ticket |
| $FDDueBy | Timestamp that denotes when the ticket is due to be resolved |
| $FDEmailConfigID | <ul><li>ID of email config which is used for this ticket`(i.e.support@yourcompany.com/sales@yourcompany.com)`</li><li>If product_id is given and email_config_id is not given, product's primary email_config_id will be set</li></ul> |
| $FDFirstResponseDueBy | Timestamp that denotes when the first response is due |
| $FDGroupID | <ul><li>ID of the group to which the ticket has been assigned</li><li>The default value is the ID of the group that is associated with the given email_config_id</li></ul> |
| $FDPriority | <ul><li>Priority of the ticket</li><li>The default value is 1</li></ul> |
| $FDProductID | ID of the product to which the ticket is associated |
| $FDRequesterID | User ID of the requester |
| $FDTicketID | ID of the created ticket  |
| $FDStatus | Status of the ticket |
| $FDsubject | Subject of the ticket |  

### Using the freshdesk API and DNIF  
The freshdesk API is found on github at 

  https://github.com/dnif/trigger-freshdesk

The following process has to be repeated on all of the following components

### Getting started with freshdesk API and DNIF

1. ####    Login to your Data Store, Correlator, and A10 containers.  
   [ACCESS DNIF CONTAINER VIA SSH](https://dnif.it/docs/guides/tutorials/access-dnif-container-via-ssh.html)
2. ####    Move to the `‘/dnif/<Deployment-key>/trigger_plugins’` folder path.
```
$cd /dnif/CnxxxxxxxxxxxxV8/trigger_plugins/
```
3. ####   Clone using the following command  
```  
git clone https://github.com/dnif/trigger-freshdesk.git freshdesk
```
4. ####   Move to the `‘/dnif/<Deployment-key>/trigger_plugins/freshdesk/’` folder path and open dnifconfig.yml configuration file     
    
   Replace the tags: <Add_your_*> with your freshdesk credentials
```
trigger_plugin:
  FD_API: <Add_your_API_key>
  FD_PASS: X
  FD_DOMAIN: <Add_your_freshdesk_domain>
```
5. #### For using userdefined templates 
   Move to the `‘/dnif/<Deployment-key>/trigger_plugins/freshdesk/’` folder path and paste your template.txt file here.
   #### Note:  
       Refer to default.txt template to create your customised templates
  
