import math

import pandas as pd


def main():
    scimagojr_df_title_and_categories = pd.read_csv("scimagojr_2019.csv", sep=";").filter(items=["Title", "Categories"])
    scopus_df_title_citations = pd.read_csv("scopus2016-2020.csv").filter(items=["Название источника", "Цитирования"])
    title_list = scimagojr_df_title_and_categories['Title'].to_list()
    categories_list = scimagojr_df_title_and_categories['Categories'].to_list()
    oecd_scopus = pd.read_excel("scopus_oecd.xlsx")
    new_categories_list = []
    list_all_categories = []

    for item in categories_list:
        item = item.replace(" (Q1)", "")
        item = item.replace(" (Q2)", "")
        item = item.replace(" (Q3)", "")
        item = item.replace(" (Q4)", "")
        new_categories_list.append(item)
    dict_title_categories = dict(zip(title_list, new_categories_list))

    for key, item in dict_title_categories.items():
        item = item.split("; ")
        dict_title_categories[key] = item

    title_list_from_dict = dict_title_categories.keys()
    categories_list_form_dict = dict_title_categories.values()

    new_scimagojr_df_title_and_categories = pd.DataFrame(
        {"Title": title_list_from_dict, "Categories": categories_list_form_dict})
    title_and_categories_and_citations_df = pd.merge(left=new_scimagojr_df_title_and_categories,
                                                     right=scopus_df_title_citations, left_on="Title",
                                                     right_on="Название источника")
    list_categories_from_df = title_and_categories_and_citations_df["Categories"].to_list()
    list_citation_form_df = title_and_categories_and_citations_df["Цитирования"].to_list()

    for elem_list in list_categories_from_df:
        for i in elem_list:
            list_all_categories.append(i)
    list_all_categories_set = list(set(list_all_categories))
    dict_all_categories = dict.fromkeys(list_all_categories_set, 0)

    for i in range(len(list_citation_form_df)):
        for key, item in dict_all_categories.items():
            if list_categories_from_df[i].count(key):
                if math.isnan(list_citation_form_df[i]):
                    list_citation_form_df[i] = 0
                dict_all_categories[key] += list_citation_form_df[i]
    result_list_categories = dict_all_categories.keys()
    result_list_citaions = dict_all_categories.values()

    result_df = pd.DataFrame({"Категория": result_list_categories, "Цитирования": result_list_citaions})
    result_df = pd.merge(left=result_df, right=oecd_scopus, left_on="Категория", right_on="направление")
    result_df.drop("Категория", axis=1, inplace=True)
    result_df.to_excel("result.xlsx", index=False)
