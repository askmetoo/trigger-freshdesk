import yaml
import os
import requests
import logging
import json
import ast
import datetime

headers = {
    'Content-Type': 'application/json',
}

path = os.environ["WORKDIR"]

try:
    with open(path + "/trigger_plugins/freshdesk/dnifconfig.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        fd_api = cfg['trigger_plugin']['FD_API']
        fd_pass = cfg['trigger_plugin']['FD_PASS']
        fd_domain = cfg['trigger_plugin']['FD_DOMAIN']
        fd_email = cfg['trigger_plugin']['FD_EMAIL']
except Exception,e:
    logging.error("FreshDesk Error in reading local DNIF Config File {}".format(e))


def select_template(dt,tmp_name):
    try:
        with open(path+"/trigger_plugins/freshdesk/"+tmp_name, "r") as f:
           ds = str(f.read())

        d = dict((x[1], '~~') for x in ds._formatter_parser())
        d.update(dt)
        c = ds.format(**d)
        c = c.replace("\n","")
        ticket = ast.literal_eval("{" + c + "}")
        url = "https://" + fd_domain + ".freshdesk.com/api/v2/tickets"
        r = requests.post(url, auth=(fd_api, fd_pass),
                          headers=headers, data=json.dumps(ticket))
        if r.status_code ==201:
            json_res=r.json()
            out = {}
            if json_res["attachments"]!=[]:
                out['$FDAttachments'] = json_res["attachments"]
            if json_res["cc_emails"] != []:
                out['$FDCCEmails'] = json_res["cc_emails"]
            if json_res["company_id"] != None:
                out['$FDCompanyID'] = json_res["company_id"]
            out['$FDCreatedAt'] = datetime.datetime.strptime((json_res["created_at"]),'%Y-%m-%dT%H:%M:%SZ').isoformat()
            if json_res["custom_fields"] !={}:
                out['$FDCustomFields'] = json_res["custom_fields"]
            out['$FDDescription'] = json_res["description_text"]
            out['$FDDueBy'] = datetime.datetime.strptime((json_res["due_by"]),'%Y-%m-%dT%H:%M:%SZ').isoformat()
            if json_res["email_config_id"] != None:
                out['$FDEmailConfigID'] = json_res["email_config_id"]
            out['$FDFirstResponseDueBy'] = datetime.datetime.strptime((json_res["fr_due_by"]),'%Y-%m-%dT%H:%M:%SZ').isoformat()
            if json_res["group_id"] != None:
                out['$FDGroupID'] = json_res["group_id"]
            out['$FDPriority'] = json_res["priority"]
            if json_res["product_id"] != None:
                out['$FDProductID'] = json_res["product_id"]
            out['$FDRequesterID'] = json_res["requester_id"]
            out['$FDTicketID'] = json_res["id"]
            out['$FDStatus'] = json_res["status"]
            out['$FDsubject'] = json_res["subject"]
            return out
    except Exception,e :
        out = {}
        s1 = "Error in API {}".format(e)
        logging.error("FDError :{}".format(e))
        out['$FDErrorMessage'] = s1
        return out


def create_ticket(inward_array, var_array):
    tmp_lst = []
    var_array[0] = var_array[0].strip()
    var_array[1] = str(var_array[1]).replace(" ","")
    for i in inward_array:
        try:
            if var_array[1] in i:
                tmp_dict = {}
                tmp_dict.update(i)
                tmp_dict['$Subject'] = str(var_array[0])+" "+str(i[var_array[1]])
                tmp_dict['$Email'] = fd_email
                if (len(var_array) == 3):
                    fname = var_array[2].replace(" ", "")
                else:
                    fname ="default.txt"
                d = select_template(tmp_dict,fname)
                i.update(d)
                tmp_lst.append(i)
        except Exception, e:
            tmp_lst.append(i)
            logging.error("%s", e)
    return tmp_lst
