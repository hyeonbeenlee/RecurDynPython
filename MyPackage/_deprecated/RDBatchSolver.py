import os
import shutil
import glob
import datetime
import subprocess

class BatchWriter:
    """
    사용 시 유의점
    Parametric Value는 지원되지 않으므로 해당 PV가 적용되는 모든 식을 직접 수정해주어야한다.
    Expression 수정은 가능하나 Expression이 적용된 Request, Variable Eq는 개별적으로 수정해야한다.
    Loop 해석 시 반드시 변경사항이 제대로 적용되는지 애니메이션, 데이터 등을 테스트 후 돌릴 것.
    """
    rdSolverDir = "C:\Program Files\FunctionBay, Inc\RecurDyn V9R4\Bin\Solver\RDSolverRun.exe"
    InitTime = f"{datetime.datetime.now():%Y-%m%d-%H%M}"
    SolverFilesFolderName = f"SolverFiles_{InitTime}"

    def SetBaseRMD(self, RMDfilepath:str):
        """변경할 대상 rmd를 읽어들이고 인스턴스 내에 저장한다"""
        self.baseRMDpath = RMDfilepath
        self.__baseDir = os.path.dirname(self.baseRMDpath)
        self.__fileRMD = open(self.baseRMDpath, 'r', encoding='UTF-8')
        self.__linesRMD = self.__fileRMD.readlines()
        self.__fileRMD.close()

    def SetSubfileExt(self, extensionList:list):
        """추후 rmd 수정 시 함께 복사할 추가 파일 확장자를 지정한다 """
        self.__modelSubfileExt = extensionList
        for idx, ext in enumerate(extensionList):
            self.__modelSubfileExt[idx] = "*." + ext
        self.modelSubfiles = []
        for ext in self.__modelSubfileExt:
            self.modelSubfiles += glob.glob(self.__baseDir + "\\" + ext)

    def SearchInRMD(self, SearchKeyword:str, PrintRange:int):
        """단순 검색 및 출력함수, SearchInRMD(string SearchKeyword rmd파일에서 찾을 키워드, int PrintRange 찾은 행에서 추가로 출력할 행의 수)"""
        for idx, line in enumerate(self.__linesRMD):
            if SearchKeyword in line:
                for j in range(PrintRange):
                    print(f"Index {idx + j}: " + self.__linesRMD[idx + j], end='')
                print()

    def InitializeEditor(self):
        """SetBaseRMD에서 불러들인 rmd내용을 복사해 인스턴스에 더미를 만든다"""
        self.__fileRMD = open(self.baseRMDpath, 'r', encoding='UTF-8')
        self.__fixlinesRMD = self.__fileRMD.readlines()
        self.__fileRMD.close()

    def EditRMD(self, **kwargs):
        """
        만들어진 더미를 수정한다
        kwargs index=int 수정할 행의 인덱스
        kwargs content=string 해당 행에 바꿔넣을 내용
        """
        self.__fixIndex = kwargs['index']
        self.__fixContent = kwargs['content']
        self.__fixContent += "\n"  # 개행 추가
        self.__fixlinesRMD[self.__fixIndex] = self.__fixContent
        print(f"Edited index {self.__fixIndex}: {self.__fixlinesRMD[self.__fixIndex]}", end='')

    def SaveRMDRSS(self, ChildDirName:str, EndTime:float, NumSteps:int):
        """
        string ChildDirName: 저장할 단일 rmd 폴더명
        float EndTime: 시뮬레이션 엔드타임
        int NumSteps: 시뮬레이션 스텝 수
        """
        Directory = f"{self.__baseDir}\\{BatchWriter.SolverFilesFolderName}\\{ChildDirName}"
        if not os.path.exists(Directory):
            os.makedirs(Directory)

        # Write RMD
        self.__NewRMDName = f"{Directory}\\{ChildDirName}.rmd"
        self.__NewfileRMD = open(self.__NewRMDName, 'w', encoding='UTF-8')
        self.__NewfileRMD.writelines(self.__fixlinesRMD)
        self.__NewfileRMD.close()
        print(f"Created: {self.__NewRMDName}")

        # Write RSS
        self.__NewRSSName = f"{Directory}\\{ChildDirName}.rss"
        self.__NewRSS = open(self.__NewRSSName, 'w', encoding='UTF-8')
        self.__NewRSS.write(f"SIM / DYN, END = {EndTime}, STEP = {NumSteps}\n")
        self.__NewRSS.write(f"STOP\n")
        self.__NewRSS.close()
        print(f"Created: {self.__NewRSSName}")

        # Copy subfiles
        for subfile in self.modelSubfiles:
            shutil.copy(subfile, Directory)

        for ext in self.__modelSubfileExt:
            print(f"Copied: {Directory}\\{ext}")
        print()

    def WriteBatch(self):
        """
        cls.SolverFilesFolderName 내의 모든 RMD파일 스캔하여 batch runner를 cls.SolverFilesFolderName내에 생성한다
        """
        self.RMDList = glob.glob(f"{self.__baseDir}\\{BatchWriter.SolverFilesFolderName}\\**\\*.rmd", recursive=True)
        BatchWriter.batfileName = f"{self.__baseDir}\\{BatchWriter.SolverFilesFolderName}\\Batch_{BatchWriter.InitTime}.bat"
        self.__fileBatch = open(BatchWriter.batfileName, "w", encoding='UTF-8')

        for RMDpath in self.RMDList:
            Directory = os.path.dirname(RMDpath)
            RMDRSSname = os.path.basename(RMDpath).replace(".rmd", "")

            Drive = Directory[:2]
            if Drive == "C:":
                self.__fileBatch.write("C:\n")
            elif Drive == "D:":
                self.__fileBatch.write("D:\n")

            self.__fileBatch.write(f"cd {Directory}\n")
            self.__fileBatch.write(f"\"{self.rdSolverDir}\" {RMDRSSname} {RMDRSSname}\n")

        # self.fileBatch.write("PAUSE") #실행 끝나고 일시정지
        self.__fileBatch.close()
        print(f"Saved Batch Runner: {BatchWriter.batfileName}\n")

    @classmethod
    def RunBatch(cls):
        print(f"Running {cls.batfileName}...")
        StartTime = datetime.datetime.now()
        subprocess.run(cls.batfileName, creationflags=subprocess.CREATE_NEW_CONSOLE)
        EndTime = datetime.datetime.now()
        Elapsed = EndTime - StartTime
        print(f"Finished, simulation time: {Elapsed}")


    def ShutDown(self):
        os.system("shutdown -s")