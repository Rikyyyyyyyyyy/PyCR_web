from fpdf import FPDF
def gen_overview_report(path,selected_variables):
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    
    # create a cell
    pdf.set_font("Arial",'B', size = 20)
    pdf.cell(200, 10, txt = "Overview Report",
            ln = 2, align = 'C')
    ## PCA graphs 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '1) PCA before Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_before_FS.png',x=10,y=40,w=84,h=70)
    pdf.image(path+'/pca/pca_graph/PCA_before_FS.png',x=120,y=40,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.cell(200, 10, txt = '2) PCA after Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_after_FS.png',x=10,y=130,w=84,h=70)
    pdf.image(path+'/pca/pca_graph/PCA_after_FS.png',x=120,y=130,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
     ## Selected variables 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '3) Selected Variables',
        ln = 1, align = 'L')
    pdf.set_font("Arial", size = 10)
    th = pdf.font_size
    for row in selected_variables:
        pdf.cell(20, 2*th, "")
        for datum in row:
            # Enter data in colums
            pdf.cell(40, 2*th, str(datum), border=1)
        pdf.ln(2*th)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    outputPath = path+"/overview_report"+".pdf"
    pdf.output(outputPath,'F')  

def gen_detail_report(path,selected_variables):
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    
    # create a cell
    pdf.set_font("Arial",'B', size = 20)
    pdf.cell(200, 10, txt = "Detail Report",
            ln = 2, align = 'C')
    ## PCA graphs 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '1) PCA before Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_before_FS.png',x=10,y=40,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_before_FS.png',x=120,y=40,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.cell(200, 10, txt = '2) PCA after Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_after_FS.png',x=10,y=130,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_after_FS.png',x=120,y=130,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    ## Selected variables 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '3) Selected Variables',
        ln = 1, align = 'L')
    pdf.set_font("Arial", size = 10)
    th = pdf.font_size
    for row in selected_variables:
        pdf.cell(20, 2*th, "")
        for datum in row:
            # Enter data in colums
            pdf.cell(40, 2*th, str(datum), border=1)
        pdf.ln(2*th)

    ## new content for detail report
    pdf.add_page()
    ## ROC graphs 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '4) ROC Iterations graph ',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 7)
    pdf.cell(200, 10, txt = '   **Depend on how many iterations you have, the color start at red and tend to be blue when the interation goes.',
        ln = 1, align = 'L')
    pdf.image(path+'/roc_curve/rocIterations/rocIterations.png',x=50,y=30,w=84,h=70)

    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    ## Loading plots
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '5) Loading Plots before FS',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/loading_plot/loading_before_FS_PC1.png',x=10,y=130,w=84,h=70)
    pdf.image(path+'/pca/loading_plot/loading_before_FS_PC2.png',x=120,y=130,w=84,h=70)
    for i in range(9):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.cell(200, 10, txt = '5) Loading Plots after FS',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 7)
    pdf.image(path+'/pca/loading_plot/loading_after_FS_PC1.png',x=10,y=220,w=84,h=70)
    pdf.image(path+'/pca/loading_plot/loading_after_FS_PC2.png',x=120,y=220,w=84,h=70)

    ## new content for detail report
    pdf.add_page()
    ## Loading plots
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '6) Start and Stop number ',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 7)
    pdf.image(path+'/additional_information/startStopNum.png',x=50,y=30,w=84,h=70)
    

    ## output the report as pdf 
    outputPath = path+"/detail_report"+".pdf"
    pdf.output(outputPath,'F')  


def main():
    path = '/Users/wenwenli/Desktop/output_stat'
    # gen_overview_report(path,[['Location','Variable Name'],['1','a'],['2','b'],['3','c'],['4','d']])
    gen_detail_report(path,[['Location','Variable Name'],['1','a'],['2','b'],['3','c'],['4','d']])


main()