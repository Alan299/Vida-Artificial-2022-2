program vectors_array;

uses math;

{References}
(*
Random gaussian
https://people.cs.nctu.edu.tw/~tsaiwn/sisc/runtime_error_200_div_by_0/www.merlyn.demon.co.uk/pas-rand.htm#G
https://sourceforge.net/p/cai/svncode/HEAD/tree/trunk/lazarus/libs/uvolume.pas#l167
*)

const
  e = 2.7182818;
  N_INPUT = 10;
  N_HIDDEN = 100;
  N_OUTPUT = 10;
  BATCH_SIZE = 8;

type
  TInput =  array[1..N_INPUT] of real;
  TOutput = array[1..N_OUTPUT] of real;
  TZ  = array[1..N_HIDDEN] of real;
  TMHidden = array[1..N_INPUT,1..N_HIDDEN] of real; {from input to hidden}
  TMOutput = array[1..N_HIDDEN,1..N_OUTPUT] of real; {from hidden to output}
  TBatch = array[1..BATCH_SIZE] of real;

var
  i,j : integer;
  INPUT: TInput;
  HIDDEN: TMHidden;
  MOUTPUT: TMOutput;
  examples: TBatch;
  labels: TBatch;
  {t_example :TList;}
  {t_label: TList;}



function sigmoid(x: real): real;
  begin
    sigmoid := (1/(1 + Power(e,-x))) ;
  end;
function relu(x: real) : real;
  begin
  relu :=   x;
  if x < 0 then
    relu := 0;
  end;

{ Marsaglia-Bray algorithm: }
function RandGaussian(Mean, StdDev : extended) : extended ;
  var U1, S2 : extended ;
  begin
    repeat
      U1 := 2*Random - 1 ;
      S2 := Sqr(U1) + Sqr(2*Random-1) ;
      until S2 < 1 ;
    RandGaussian := Sqrt(-2*Ln(S2)/S2) * U1 * StdDev + Mean ;
  end ;

function rnorm (mean, sd: real): real;
  {Calculates Gaussian random numbers according to the Box-Müller approach}
   var
    u1, u2: real;
  begin
    randomize;
    u1 := random;
    u2 := random;
    rnorm := mean * abs(1 + sqrt(-2 * (ln(u1))) * cos(2 * pi * u2) * sd);
   end;

procedure print_hidden(M: TMHidden);
var i,j : integer;
begin
for i:= 1 to N_INPUT do
  begin
  for j:=1 to N_HIDDEN do
    write(M[i,j], ' ');
  end;
end;


procedure print_z(z: TZ );
var j : integer;
begin
writeln('Writing Z: ');
for j:=1 to N_HIDDEN do
  write(z[j], ' ');
end;

procedure init_hidden(var M: TMHidden);
var i,j :integer;
sd: real; {standard deviation for random normal}
begin
randomize;
sd := (1/(sqrt(N_INPUT*1.0)));
for i:= 1 to N_INPUT do
  begin
  for j:=1 to N_HIDDEN do
    M[i,j] := RandGaussian(0, sd); {rnorm(0,sd );}
  end;
end;


procedure init_ouput(var M: TMOutput);
var i,j :integer;
sd: real; {standard deviation for random normal}
begin
randomize;
sd := (1/(sqrt(N_INPUT*1.0)));
for i:= 1 to N_HIDDEN do
  begin
  for j:=1 to N_OUTPUT do
    M[i,j] := RandGaussian(0, sd); {rnorm(0,sd );  }
  end;
end;

procedure init_input_ones(var input: TInput);
var
  i: integer;
begin
  for i :=1 to N_INPUT do
    input[i] := 1;
end;

{Mean square error loss function}
function loss(y, y_: TBatch) : real;
  var
    i,n: integer;

    d,s: real;
  begin
  n := length(y);
  s := 0;
  for i := 1 to n do
    begin
    d:= (y[i] - y_[i]);
    s:= s+ d*d;
    end;
    s := s/n;
  loss :=  s;
  end;



function forward(input: TInput ) :  TOutput;
var
  i,j: integer;
  Z: TZ;
  s: real;
  OUTPUT: TOutput;

begin

  {Z = activation(input * HIDDEN)  }
  for i := 1 to N_HIDDEN do
    begin
    s := 0;
    for j := 1 to N_INPUT do
      begin
      s := s + (input[j] * HIDDEN[j,i]);
      end;
    Z[i] := s;
    end;

    {print_z(Z);}

    {OUTPUT =activation(Z * MOUTPUT) }

    for i := 1 to N_OUTPUT do
    begin
      s:= 0;
      for j := 1 to N_HIDDEN do
        begin
        s := s + Z[i] * MOUTPUT[j,i];
        end;
      OUTPUT[i] := s;
    end;

    forward := OUTPUT;
end;

begin
  writeln('INIT');


  init_hidden(HIDDEN);
  print_hidden(HIDDEN);

  writeln();
  writeln('Scale:  ', (1/(sqrt(N_INPUT*1.0)))  );
  writeln('random number: ', rnorm(0, (1/(sqrt(N_INPUT*1.0)))));
  writeln('random number: ',randg(0,1));
  writeln('random number: ',RandGaussian(0,(1/(sqrt(N_INPUT*1.0)))   )  );

  init_input_ones(INPUT);
  forward(INPUT);


  writeln('Relu(0) : ', relu(0), relu(1), relu(-5), relu(23131));

  for i:= 1 to BATCH_SIZE do
    examples[i] := 1.0;

  for i  := 1 to BATCH_SIZE do
    labels[i] := 2.0;


  write('Loss: ', loss(examples, labels));
end.
