��    +      t  ;   �      �  ,   �  %   �          ,     L     X     e     l     �  �   �  g   2     �     �  '   �  �   �     �     �  -   �  o     m   {  i   �  n   S     �     �  �  �     �
     �
     �
  x   �
     n  �  �       �     :   �     ,  ;   F  e   �  >   �  �   '       
   $  *   /  �  Z  *   /  '   Z     �     �     �     �     �     �     �  �     a   �            (   "  �   K     "     <  0   J  s   {  p   �  o   `  l   �     =     D  �  ^     ,     2     N  j   e     �  �  �     p  �   �  R   J     �  R   �  k     =   r  �   �     �     �  *   �                  )                    +         (                
           %         !                    	                                  &   '      *                   $   "              #               %attach%. Path to current attachments folder %folder%. Path to current page folder %html%. Current page. HTML file %page%. Current page. Text file All Files|* Append Tools Button Can't execute tools Can't save options Create a link for running application.exe with parameters:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code> Creating a link for running application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code> Error Examples Executables (*.exe)|*.exe|All Files|*.* Execute application.exe from attachments folder:
<code><pre>(:exec:)
%attach%/application.exe %attach%/my_file.txt
(:execend:)</pre></code>
or
<code><pre>(:exec:)
Attach:application.exe Attach:my_file.txt
(:execend:)</pre></code> External Tools [Plugin] ExternalTools ExternalTools plugin. Insert (:exec:) command ExternalTools plugin. Insert a %attach% macros. The macros will be replaced by a path to current attach folder. ExternalTools plugin. Insert a %folder% macros. The macros will be replaced by a path to current page folder. ExternalTools plugin. Insert a %html% macros. The macros will be replaced by a path to current HTML file. ExternalTools plugin. Insert a %page% macros. The macros will be replaced by a path to current page text file. Format Inserting (:exec:) command Inside (:exec:) command may be macroses. The macroses will be replaced by appropriate paths:
<ul>
<li><b>%page%</b>. The macros will be replaced by full path to page text file.</li>
<li><b>%html%</b>. The macros will be replaced by full path to HTML content file.</li>
<li><b>%folder%</b>. The macros will be replaced by full path to page folder.</li>
<li><b>%attach%</b>. The macros will be replaced by full path to attach folder without slash on the end.</li>
</ul> Link Open Content File with... Open Result HTML File with... Open attached file with application.exe:
<code><pre>(:exec:)
application.exe Attach:my_file.txt
(:execend:)</pre></code> Open file dialog... Open notes files with external editor.

For OutWiker 1.9 and above ExternalTools adds the (:exec:) command for creation link or button for execute external applications from wiki page.

The (:exec:) command allow to run many applications. Every application must writed on the separated lines.

If line begins with "#" this line will be ignored. "#" in begin of the line is sign of the comment.
 Remove tool Run a lot of applications:
<code><pre>(:exec text="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code> Run application by ExternalTools plugin?
It may be unsafe. Run applications (:exec:) Run applications by ExternalTools plugin?
It may be unsafe. Same but creating a button
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code> Show warning before executing applications by (:exec:) command The (:exec:) command has the following optional parameters:
<ul>
<li><b>format</b>. If the parameter equals "button" command will create a button instead of a link.</li>
<li><b>title</b>. The parameter sets the text for link or button.</li>
</ul> Title Tools List http://jenyay.net/Outwiker/ExternalToolsEn Project-Id-Version: outwiker
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2015-05-14 23:10+0300
PO-Revision-Date: 2016-08-02 09:25+0300
Last-Translator: Jenyay <jenyay.ilin@gmail.com>
Language-Team: Swedish
Language: sv_SE
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
X-Generator: Poedit 1.8.7.1
X-Crowdin-Project: outwiker
X-Crowdin-Language: sv-SE
X-Crowdin-File: externaltools.po
 %attach%. Sökväg till aktuell bilagemapp %folder%. Sökväg till aktuell sidmapp %html%. Aktuell sida. HTML-fil %page%. Aktuell sida. Textfil Alla filer|* Tillämpa verktyg Knapp Kan inte starta verktyg Kan inte spara alternativ Skapa en länk för att köra program.exe med parametrar:
<code><pre>(:exec:)
program.exe parameter1 "c:\din mapp\sökväg till fil"
(:execend:)</pre></code> Skapa en länk för att köra program.exe:
<code><pre>(:exec:)program.exe(:execend:)</pre></code> Fel Exempel Exekverbara (*.exe)|*.exe|Alla filer|*.* Starta program.exe från bilagemappen:
<code><pre>(:exec:)
%attach%/program.exe %attach%/din_fil.txt
(:execend:)</pre></code>
eller
<code><pre>(:exec:)
Attach:program.exe Attach:din_fil.txt
(:execend:)</pre></code> Externa verktyg [Instick] ExternalTools ExternalTools-instick. Infoga kommandot (:exec:) ExternalTools-instick. Infoga ett %attach%-makro. Makrot kommer att ersättas med sökväg till aktuell bilagemapp. ExternalTools-instick. Infoga ett %folder%-makro. Makrot kommer att ersättas med sökväg till aktuell sidmapp. ExternalTools-instick. Infoga ett %html%-makro. Makrot kommer att ersättas med sökväg till aktuell HTML-fil. ExternalTools-instick. Infoga ett %page% -makro. Makrot kommer att ersättas med sökväg till aktuell sida. Format Infoga kommandot (:exec:) (:exec:)-kommandot kan innehålla makron. Makron ersätts med respektive sökväg:
<ul>
<li><b>%page%</b>. Makrot ersätts med fullständig sökväg till sidans textfil.</li>
<li><b>%html%</b>. Makrot ersätts med fullständig sökväg till HTML-filen.</li>
<li><b>%folder%</b>. Makrot ersätts med fullständig sökväg till sidmappen.</li>
<li><b>%attach%</b>. Makrot ersätts med fullständig sökväg till bilagemappen utan avslutande snedstreck.</li>
</ul> Länk Öppna innehållsfil med... Öppna HTML-fil med... Öppna bilaga med program.exe:
<code><pre>(:exec:)
program.exe Attach:din_fil.txt
(:execend:)</pre></code> Öppna fildialog... Öppna notisfiler med extern redigerare.

I OutWiker 1.9 och senare, lägger ExternalTools till (:exec:)-kommandot som skapar länk eller knapp för körning av externa program från wiki-sidan.

(:exec:)-kommandot låter dig köra flera program. Varje program måste anges på separat rad.

Om raden börjar med "#" kommer den att undantas. "#" i början på en rad är tecknet för kommentar.
 Ta bort verktyg Kör flera program:
<code><pre>(:exec text="Kör program_1, program_2 och program_3":)
program_1.exe
program_2.exe parameter_1 parameter_2
program_3.exe parameter_1 parameter_2
(:execend:)</pre></code> Vill du köra program via ExternalTools-insticket?
Det kan vara en säkerhetsrisk. Kör program (:exec:) Vill du köra program via ExternalTools-insticket?
Det kan vara en säkerhetsrisk. Samma, fast skapa en knapp istället
<code><pre>(:exec format=button:)
program.exe
(:execend:)</pre></code> Visa varning före körning av program via (:exec:)-kommandot (:exec:)-kommandot har följande tilläggsparametrar:
<ul>
<li><b>format</b>. Om parametern är "button" skapar kommandot en knapp istället för en länk.</li>
<li><b>title</b>. Parametern anger texten som länk eller knapp.</li>
</ul> Titel Verktygslista http://jenyay.net/Outwiker/ExternalToolsEn 