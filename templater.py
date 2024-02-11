from jinja2 import Environment, FileSystemLoader, Template
from dataclasses import dataclass
import pandas as pd
import numpy as np
import octk
import os


class HeaderMapping:
    bot_id = "ID"
    priority = "Final Priority (Numbered Order)"
    bot_name = "Bot Name"
    description = "Description"
    technology = "Technology"
    app_architecture = "App Architecture"
    process = "Process"
    applications = "Applications"
    inputs = "Inputs"
    outputs = "Outputs"
    bot_authors = "Bot Author(s)"
    paths = "Path to main script file"
    autobots_project_id = "Autobots Project ID"
    usage_data_source = "Usage Data Source"
    bot_user_team = "Users of the bot (Business Team / Ops Team)"
    demo_status = "Demo Status"
    demo_status_date = "Demo Status Date"
    demo_recording_link = "Demo Recording Link"
    onboarded_to_bpo = "Onboarded to TCS BPO"
    owner = "Owner"
    process_owner_contact = "Process Owner contact"
    demonstration_contact = "Demonstration Contact"


@dataclass
class BotInfo:
    bot_id: str
    priority: str
    bot_name: str
    description: str
    technology: str
    app_architecture: str
    process: str
    applications: str
    inputs: str
    outputs: str
    bot_authors: str
    paths: str
    autobots_project_id: str
    usage_data_source: str
    bot_user_team: str
    demo_status: str
    demo_status_date: str
    demo_recording_link: str
    onboarded_to_bpo: str
    owner: str
    process_owner_contact: str
    demonstration_contact: str


    def create_readme(self, template:Template, output_path:str):
        with open(output_path, "w") as file:
            file.write(template.render(self.__dict__))


                
        

environment = Environment(loader=FileSystemLoader("templates"))
template = environment.get_template("readme_template.md")


def clean_df(df) -> pd.DataFrame:
    df[HeaderMapping.priority] = pd.to_numeric(
        df[HeaderMapping.priority], errors='coerce'
        ).fillna(0).astype(int).astype(str).str.zfill(3).replace('000', 'N/A')
    
    df[HeaderMapping.bot_id] = pd.to_numeric(
        df[HeaderMapping.bot_id], errors='coerce'
        ).astype(str).str.zfill(3)
    
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.replace('\n', ' - ') if isinstance(x, str) else x)

    def date_format(x):
        import datetime as dt
        try:
            return dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        except:
            return x
        
    df[HeaderMapping.demo_status_date].apply(date_format)


    return df



def create_bot_info_instances(file_path):
    
    df = pd.read_excel(file_path, dtype={HeaderMapping.demo_status_date: str})  # Read the Excel file into a DataFrame
    df = clean_df(df)

    bot_info_instances = []

    for _, row in df.iterrows():
        bot_info = BotInfo(
            bot_id = row[HeaderMapping.bot_id],
            priority = row[HeaderMapping.priority],
            bot_name = row[HeaderMapping.bot_name],
            description = row[HeaderMapping.description],
            technology = row[HeaderMapping.technology],
            app_architecture = row[HeaderMapping.app_architecture],
            process = row[HeaderMapping.process],
            applications = row[HeaderMapping.applications],
            inputs = row[HeaderMapping.inputs],
            outputs = row[HeaderMapping.outputs],
            bot_authors = row[HeaderMapping.bot_authors],
            paths = row[HeaderMapping.paths],
            autobots_project_id = row[HeaderMapping.autobots_project_id],
            usage_data_source = row[HeaderMapping.usage_data_source],
            bot_user_team = row[HeaderMapping.bot_user_team],
            demo_status = row[HeaderMapping.demo_status],
            demo_status_date = row[HeaderMapping.demo_status_date],
            demo_recording_link = row[HeaderMapping.demo_recording_link],
            onboarded_to_bpo = row[HeaderMapping.onboarded_to_bpo],
            owner = row[HeaderMapping.owner],
            process_owner_contact = row[HeaderMapping.process_owner_contact],
            demonstration_contact = row[HeaderMapping.demonstration_contact],
        )
        bot_info_instances.append(bot_info)

    return bot_info_instances

bot_info_instances = create_bot_info_instances("bot_data.xlsx")

output_dir = octk.uniquify("test/outputs/output")
os.makedirs(output_dir, exist_ok=True)

for bot_info in bot_info_instances:
    bot_info.create_readme(template, f"{output_dir}/{bot_info.bot_id}.md")
