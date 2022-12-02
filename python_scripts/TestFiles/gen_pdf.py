from fpdf import FPDF
# generate PDF report 
# Input: path-> saving address, selected_variables-> selected variable after feature selection['position','variable name']
# generate PDF report 
# Input: path-> saving address, selected_variables-> selected variable after feature selection['position','variable name']
def gen_overview_report(path,selected_variables,taskName,validationData,rankingAlgorithm,rocType,tupaType,scaleType,iterations,survivalRate,Normalization,nComponent):
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    pdf.set_font("Arial",'B', size = 20)
    pdf.cell(200, 10, txt = "Overview Report",
            ln = 2, align = 'C')
    for i in range(2):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = "Task Settings",
            ln = 2, align = 'L')
    pdf.set_font("Arial", size = 10)
    # create a cell
    pdf.cell(200, 10, txt = 'Task Name: ' + taskName,
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'Data Validation: ' + validationData,
    ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'Preprocessing: '+ tupaType +' '+Normalization+' '+scaleType,
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'Number of component: ' + str(nComponent),
    ln = 2, align = 'L')
    for i in range(1):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = "Feature Selection Settings",
            ln = 2, align = 'L')
    pdf.set_font("Arial", size = 10)
    pdf.cell(200, 10, txt = 'Variable Ranking Algorithm: ' + rankingAlgorithm,
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt ='How Many Iteration: ' + str(iterations),
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt ='Survival Rate: ' + str(survivalRate) ,
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'Roc Type: '+ rocType,
        ln = 2, align = 'L')
    pdf.add_page()
    # set style and size of font
    # that you want in the pdf
    # set style and size of font
    # that you want in the pdf
    
    # create a cell
    pdf.set_font("Arial",'B', size = 15)
    pdf.cell(200, 10, txt = "Overview Report",
            ln = 2, align = 'C')

    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = '1) PCA plots',
        ln = 1, align = 'L')
    ## PCA graphs 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '  a) PCA before Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_before_FS.png',x=10,y=40,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_before_FS.png',x=120,y=40,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.cell(200, 10, txt = '  b) PCA after Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_after_FS.png',x=10,y=130,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_after_FS.png',x=120,y=130,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
     ## Selected variables 
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = '2) Selected Variables',
        ln = 1, align = 'L')
    pdf.set_font("Arial", size = 10)
    th = pdf.font_size
    selected_variables = [['Index','Variable Name']] + selected_variables
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

def gen_detail_report(path,selected_variables,roc_name,taskName,validationData,rankingAlgorithm,rocType,tupaType,scaleType,iterations,survivalRate,Normalization,nComponent):
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    pdf.set_font("Arial",'B', size = 20)
    pdf.cell(200, 10, txt = "Overview Report",
            ln = 2, align = 'C')
    for i in range(2):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = "Task Settings",
            ln = 2, align = 'L')
    pdf.set_font("Arial", size = 10)
    # create a cell
    pdf.cell(200, 10, txt = 'Task Name: ' + taskName,
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'Data Validation: ' + validationData,
    ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'Preprocessing: '+ tupaType +' '+Normalization+' '+scaleType,
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'Number of component: ' + str(nComponent),
    ln = 2, align = 'L')
    for i in range(1):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = "Feature Selection Settings",
            ln = 2, align = 'L')
    pdf.set_font("Arial", size = 10)
    pdf.cell(200, 10, txt = 'Variable Ranking Algorithm: ' + rankingAlgorithm,
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt ='How Many Iteration: ' + str(iterations),
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt ='Survival Rate: ' + str(survivalRate) ,
        ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'Roc Type: '+ rocType,
        ln = 2, align = 'L')
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    
    # create a cell
    pdf.set_font("Arial",'B', size = 15)
    pdf.cell(200, 10, txt = "Detailed Report",
            ln = 2, align = 'C')
    ## PCA graphs 
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = '1) PCA plots',
        ln = 1, align = 'L')
    ## PCA graphs 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '  a) PCA before Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_before_FS.png',x=10,y=40,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_before_FS.png',x=120,y=40,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.cell(200, 10, txt = '  b) PCA after Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_after_FS.png',x=10,y=130,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_after_FS.png',x=120,y=130,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    ## Selected variables 
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = '2) Selected Variables',
        ln = 1, align = 'L')
    pdf.set_font("Arial", size = 10)
    th = pdf.font_size
    selected_variables = [['Index','Variable Name']] + selected_variables
    for row in selected_variables:
        pdf.cell(20, 2*th, "")
        for datum in row:
            # Enter data in colums
            pdf.cell(40, 2*th, str(datum), border=1)
        pdf.ln(2*th)

    ## new content for detail report
    pdf.add_page()
    ## ROC graphs 
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = '3) ROC Curve ',
        ln = 1, align = 'L')
    pdf.set_font("Arial", size = 7)
    pdf.cell(200, 10, txt = '   ** The initial Roc Curve starts with red and graduly progresses to blue as iterations increase.',
        ln = 1, align = 'L')
    img_x = 10
    img_y = 40
    counter = 0
    for name in roc_name:
        if img_x == 230:
            img_x = 10
        if img_y == 220:
            img_y = 40
        pdf.image(path+'/roc_curve/rocIterations/'+name,img_x,img_y,w=84,h=70)
        counter = counter +1
        if counter%2:
            img_x = img_x+110
        else:
            img_y = img_y +90
        

    ## new content for detail report
    pdf.add_page()
    ## Loading plots
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = '4) Loading Plots before FS',
        ln = 1, align = 'L')
    pdf.set_font("Arial", size = 7)
    pdf.cell(200, 10, txt = '   ** The actual loadings values are included in the [additional information] folder. ',ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '  a) Loading Plots after FS',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/loading_plot/loading_before_FS_PC1.png',x=10,y=40,w=84,h=70)
    pdf.image(path+'/pca/loading_plot/loading_before_FS_PC2.png',x=120,y=40,w=84,h=70)
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.cell(200, 10, txt = '  b) Loading Plots after FS',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/loading_plot/loading_after_FS_PC1.png',x=10,y=130,w=84,h=70)
    pdf.image(path+'/pca/loading_plot/loading_after_FS_PC2.png',x=120,y=130,w=84,h=70)

    ## new content for detail report
    pdf.add_page()
    ## Loading plots
    pdf.set_font("Arial",'B', size = 13)
    pdf.cell(200, 10, txt = '5) Start and Stop number ',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 7)
    pdf.image(path+'/additional_information/startStopNum.png',x=50,y=30,w=84,h=70)
    

    ## output the report as pdf 
    outputPath = path+"/detail_report"+".pdf"
    pdf.output(outputPath,'F')


def main():
    path = '/Users/wenwenli/Desktop/output_urain1'
    gen_overview_report(path,[['Location','Variable Name'],['1','a'],['2','b'],['3','c'],['4','d']],'task1','internal','fisher','multi-roc','no tupa','auto scale',10,0.85,'no norm',2)
    gen_detail_report(path,[['Location','Variable Name'],['1','a'],['2','b'],['3','c'],['4','d']],['rocIterations.png'],'task1','internal','fisher','multi-roc','no tupa','auto scale',100,0.85,'no norm',2)


main()