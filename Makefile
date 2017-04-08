testworkflow:
	#./run_testclass.sh tests.test_workflow.TestWorkflow
	#./run_testclass.sh tests.test_workflow.TestWorkflowWithSimpleRW
	#./run_testclass.sh tests.test_workflow.TestRequestScale
	#./run_testclass.sh tests.test_workflow.TestUniformDataLifetime
	#./run_testclass.sh tests.test_workflow.TestLocality
	#./run_testclass.sh tests.test_workflow.TestAlignment
	#./run_testclass.sh tests.test_workflow.TestTraceOnly
	#./run_testclass.sh tests.test_workflow.Test_TraceAndSimulateNKFTL
	./run_testclass.sh tests.test_workflow.Test_TraceAndSimulateNKFTL

testone:
	#./run_testclass.sh tests.misc_test.TestClassifyGcLOG
	#./run_testclass.sh tests.test_nkftl.TestLogGroup2
	#./run_testclass.sh tests.test_workflow.TestWorkflow
	#./run_testclass.sh tests._workrunner.test_workload.TestPatternSuite
	./run_testclass.sh tests.test_parameterpool.TestParameterPool

collectparadicts:
	sudo python -m benchmarks.appbench -t 'collect_para_dicts()'

testmisc:
	./run_testclass.sh tests.misc_test

runlocalbwsim:
	sudo python -m benchmarks.appbench -t 'run_from_para_dict_json()'

simevents:
	sudo python -m benchmarks.appbench -t 'simulate_from_event_files(app="$(app)", rule="$(rule)", expname="$(expname)")'

appmix4rw:
	sudo python -m benchmarks.appbench -t 'appmixbench_for_rw(testsetname="$(testsetname)", expname="$(expname)")'

test:
	sudo python -m unittest discover -s tests -v -p '*test*.py' > tmp

testblockpools:
	./run_testclass.sh tests.test_devblockpool && ./run_testclass.sh tests.test_tagblockpool  && ./run_testclass.sh tests.test_blockpool

testnkftl:
	./run_testclass.sh tests.test_nkftl

testcontractbench:
	./run_testclass.sh tests._accpatterns.test_contractbench

patternbench:
	sudo python -m benchmarks.patternbench -t "pattern_on_fs()"

fiobench:
	sudo python -m benchmarks.fiobench -t 'compare_fs()'

appbench:
	sudo python -m benchmarks.appbench -t 'bench()'

reproduce:
	sudo python -m benchmarks.appbench -t 'reproduce()'

lbawearbench:
	sudo python -m benchmarks.lbawearbench -t 'wearleveling_bench()'

contractbench:
	sudo python -m benchmarks.lbabench -t 'contract_bench()'

leveldb:
	sudo python -m benchmarks.appbench -t 'leveldbbench()'

leveldb4alignment:
	sudo python -m benchmarks.appbench -t 'leveldbbench_for_alignment()'

leveldb4locality:
	sudo python -m benchmarks.appbench -t 'leveldbbench_for_locality()'

leveldb4wearleveling:
	sudo python -m benchmarks.appbench -t 'leveldbbench_for_wearleveling()'

sqlite4locality:
	sudo python -m benchmarks.appbench -t 'sqlitebench_for_locality()'

sqlite:
	sudo python -m benchmarks.appbench -t 'sqlitebench()'

appmix:
	sudo python -m benchmarks.appbench -t 'appmixbench()'

appmix4lpncount:
	sudo python -m benchmarks.appbench -t 'appmixbench_for_lpn_count()'


appmix4scaling:
	sudo python -m benchmarks.appbench -t 'appmixbench_for_scaling()'


appmix4wearleveling:
	sudo python -m benchmarks.appbench -t 'appmixbench_for_wearleveling()'

appmix4bw:
	sudo python -m benchmarks.appbench -t 'appmixbench_for_bw()'

sqlite4alignment:
	sudo python -m benchmarks.appbench -t 'sqlitebench_for_alignment()'

varmail:
	sudo python -m benchmarks.appbench -t 'varmailbench()'

varmail4alignment:
	sudo python -m benchmarks.appbench -t 'varmailbench_for_alignment()'

varmail4locality:
	sudo python -m benchmarks.appbench -t 'varmailbench_for_locality()'

newsqlbench:
	sudo python -m benchmarks.appbench -t 'newsqlbench()'

filesnake:
	sudo python -m benchmarks.appbench -t 'filesnakebench()'

f2fsgc:
	mkdir -p bin
	cd ./foreign && gcc -o forcef2fsgc forcef2fsgc.c && mv forcef2fsgc ../bin/

testncqparser:
	./run_testclass.sh tests.misc_test.TestNCQParser

testpara:
	./run_testclass.sh tests.test_parameterpool

